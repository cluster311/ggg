import time
from datetime import timedelta, datetime

from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.conf import settings, Settings
from sisa.renaper import Renaper
from sss_beneficiarios_hospitales.data import DataBeneficiariosSSSHospital

from obras_sociales.models import ObraSocial, ObraSocialPaciente
from recupero.models import Prestacion, Factura, FacturaPrestacion
from .models import Consulta, CarpetaFamiliar, Receta, Derivacion, Paciente, EmpresaPaciente
from especialidades.models import MedidasAnexasEspecialidad, MedidaAnexaEnConsulta
from especialidades.forms import MedidaAnexaEnConsultaForm, MedidaAnexaEnConsultaFormset
from calendario.models import Turno
from .forms import (EvolucionForm, ConsultaForm,
                    RecetaFormset, DerivacionFormset,
                    PrestacionFormset, CarpetaFamiliarForm, PacienteFormPopUp)
from recupero.forms import FacturaPrestacionFormSet
from crispy_forms.utils import render_crispy_form
import logging
from django.utils.timezone import now


logger = logging.getLogger(__name__)


def PacienteCreatePopup(request):
    form = PacienteFormPopUp(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopupCleanField(window, "%s", "%s" );</script>' % (
                instance.pk, instance.numero_documento))
    return render(request, "pacientes/paciente_createview.html", {"form": form})


class ConsultaListView(PermissionRequiredMixin, ListView):
    """
    Lista de consultas de un paciente para la interfaz del profesional.
    """

    model = Consulta
    permission_required = ("pacientes.view_consulta",)
    template_name = "pacientes/consulta_listview.html"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dni = self.kwargs["dni"]
        consultas = Consulta.objects.filter(paciente__numero_documento=dni)
        context["consultas"] = consultas

        return context


class ConsultaDetailView(PermissionRequiredMixin, DetailView):
    """
    Detalle de un objeto Consulta
    """

    model = Consulta
    permission_required = ("pacientes.view_consulta",)
    template_name = "pacientes/consulta_detailview.html"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = self.object.created.strftime("%d/%m/%Y")

        return context


class ConsultaMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = getattr(self, 'object', None)

        data = self.request.POST if self.request.method == "POST" else None
        context["data"] = data
        if data is not None:
            logger.info(f'POST consulta {data}')

        context["recetas_frm"] = RecetaFormset(data, prefix='Recetas', instance=instance)
        context["derivaciones_frm"] = DerivacionFormset(data, prefix='Derivaciones', instance=instance)
        context["prestaciones_frm"] = PrestacionFormset(data, prefix='Prestaciones', instance=instance)

        context["formsets"] = [
            context["recetas_frm"],
            context["derivaciones_frm"],
            context["prestaciones_frm"]
        ]

        context['instance'] = instance
        # se requieren las consultas anteriores como historia clínica
        if instance is None or instance.paciente is None:
            context['consultas_previas'] = None
        else:
            # evitar la consulta automática que se creo en relacion al turno
            consultas_previas_completas = []
            consultas_previas = Consulta.objects.filter(
                paciente=instance.paciente
            ).exclude(pk=instance.pk).exclude(
                turno__estado__in=[Turno.ASIGNADO, Turno.ESPERANDO_EN_SALA, Turno.CANCELADO_PACIENTE]).order_by(
                '-created')
            for cp in consultas_previas:
                mac = MedidaAnexaEnConsulta.objects.filter(consulta=cp)
                rec = Receta.objects.filter(consulta=cp)
                der = Derivacion.objects.filter(consulta=cp)
                pre = Prestacion.objects.filter(consulta=cp)
                consultas_previas_completas.append((cp, mac, rec, der, pre))
            context['consultas_previas'] = consultas_previas_completas

        consulta = self.object
        medidas_a_tomar = MedidasAnexasEspecialidad.objects.filter(
            especialidad=consulta.especialidad
        )
        for medida in medidas_a_tomar:
            MedidaAnexaEnConsulta.objects.get_or_create(
                consulta=consulta,
                medida=medida.medida
            )
        context["recetas_frm"] = RecetaFormset(data, prefix='Recetas', instance=instance)
        context["medidas_frm"] = MedidaAnexaEnConsultaFormset(data, prefix='Medidas', instance=instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()

        rs = context["recetas_frm"]
        ds = context["derivaciones_frm"]
        ps = context["prestaciones_frm"]
        ms = context["medidas_frm"]

        self.object = form.save()
        logger.info(f'Pasando el turno {self.object.turno} a "atendido"')
        # avisar al turno que fue atendido
        self.object.turno.estado = Turno.ATENDIDO
        self.object.turno.save()

        if rs.is_valid():
            rs.instance = self.object
            rs.save()

        if ds.is_valid():
            ds.instance = self.object
            ds.save()

        if ps.is_valid():
            ps.instance = self.object
            ps.save()

        # ISSUE usar MedidaAnexaEnConsultaForm
        # https://github.com/cluster311/ggg/issues/120
        if ms.is_valid():
            ms.instance = self.object
            ms.save()

        # Creación/Actualización de la Factura en base a la Consulta
        consulta = self.object

        # La factura se actualiza con los nuevos datos
        # Si no existe se crea una nueva
        factura, created = Factura.objects.update_or_create(
            consulta=consulta,
            defaults = {
                'profesional': consulta.profesional,
                'especialidad': consulta.especialidad,
                'obra_social': consulta.obra_social,
                'fecha_atencion': consulta.fecha,
                'centro_de_salud': consulta.turno.servicio.centro,
                'paciente': consulta.paciente,
                'codigo_cie_principal': consulta.codigo_cie_principal,
            }
        )

        # Agregar códigos CIE secundarios a la factura
        cod_secundarios = [cod for cod in consulta.codigos_cie_secundarios.all()]
        factura.codigos_cie_secundarios.set(cod_secundarios)

        # Crear formset de prestaciones de la factura
        # con los datos de prestaciones de la consulta
        prestaciones = FacturaPrestacionFormSet(ps.data, prefix='Prestaciones', instance=factura)

        if prestaciones.is_valid():
            prestaciones.save()

        return super().form_valid(form)


class EvolucionUpdateView(ConsultaMixin,
                          SuccessMessageMixin,
                          UserPassesTestMixin,
                          PermissionRequiredMixin,
                          UpdateView):
    """Evolución /Consulta de paciente"""
    model = Consulta
    permission_required = ("pacientes.add_consulta",)
    template_name = "pacientes/evolucion.html"
    form_class = EvolucionForm
    success_message = "Datos guardados con éxito."
    raise_exception = True

    def test_func(self):
        # ver si este profesional es el dueño de la consulta
        user = self.request.user
        pk = self.kwargs['pk']
        return Consulta.objects.filter(pk=pk, profesional__user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evolución Paciente'

        return context

    def get_success_url(self):
        return reverse(
            "profesionales.home",
        )


class CarpetaFamiliarCreateView(PermissionRequiredMixin,
                                CreateView,
                                SuccessMessageMixin):
    model = CarpetaFamiliar
    success_message = "Carpeta creada con éxito."
    form_class = CarpetaFamiliarForm
    permission_required = ("calendario.can_schedule_turno",)

    # descomentar si queremos un boton con link arriba a la derecha
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Carpeta Familiar'
    #     context['subtitle'] = 'Nueva Carpeta Familiar'
    #     context['title_url'] = 'profesionales.lista'
    #     return context

    def get_success_url(self):
        return reverse(
            "calendario.agendar"
        )


def actualizar_obra_social(paciente):
    time.sleep(2)
    dbh = DataBeneficiariosSSSHospital(user=settings.USER_SSS, password=settings.PASS_SSS)
    res = dbh.query(dni=paciente.numero_documento)
    if res['ok']:
        tablas = res['resultados']['tablas']
        data = tablas[0]['data']
        oss_data = tablas[1]['data']
        oss_codigo = (''.join(filter(str.isdigit, oss_data['Código de Obra Social'])))
        oss, created = ObraSocial.objects.get_or_create(
            codigo=oss_codigo,
            defaults={
                'nombre': oss_data['Denominación Obra Social'],
            })
        ObraSocialPaciente.objects.get_or_create(
            paciente=paciente,
            obra_social=oss,
            defaults={'data_source': settings.SOURCE_OSS_SSS,
                      'obra_social_updated': now(),
                      'tipo_beneficiario': data['Parentesco'].lower()}
        )
    else:
        rena = Renaper(dni=paciente.numero_documento)
        if rena.rnos is not None and rena.rnos != '':
            value_default = {"nombre": rena.cobertura_social}
            oss, created = ObraSocial.objects.get_or_create(
                codigo=rena.rnos, defaults=value_default
            )
            ObraSocialPaciente.objects.get_or_create(
                data_source=settings.SOURCE_OSS_SISA,
                paciente=paciente,
                obra_social_updated=now(),
                obra_social=oss,
            )


def buscar_paciente_general(dni):
    if Paciente.objects.filter(numero_documento=dni).exists():
        paciente = Paciente.objects.get(numero_documento=dni)
        if paciente.ultima_actualizacion + timedelta(days=settings.REVISE_DATA_DAYS) < datetime.now().date():
            actualizar_obra_social(paciente)
            paciente.ultima_actualizacion = datetime.now().date()
            paciente.save()
        return paciente
    else:
        # tomar todos los datos de SSS y los de SISA/PUCO

        # PRIMERO SISA porque separa bien apeelido y nombre
        # (el primero que llega crea el paciente, el segundo no modifica el nombre)
        guardado1, paciente1 = Paciente.create_from_sisa(dni)
        guardado2, paciente2 = Paciente.create_from_sss(dni)
        
        # cualquiera de los dos debe estar OK para devolver
        if isinstance(paciente1, Paciente):
            return paciente1
        if isinstance(paciente2, Paciente):
            return paciente2

        # Si ninguno de los dos anduvo entonces hay error

    return None


def BuscarPacienteRecupero(request, dni):
    if not request.user.has_perm('pacientes.add_paciente') and not request.user.has_perm('pacientes.change_paciente'):
        data = {"encontrado": False}
        return JsonResponse(data, status=400)
    dni_parseado = (''.join(filter(str.isdigit, dni)))
    paciente = buscar_paciente_general(dni_parseado)
    if paciente:
        empresa_paciente = EmpresaPaciente.objects.select_related('empresa').filter(paciente_id=paciente.id).order_by('-id')
        if empresa_paciente:
            empresa = {
                "encontrado": True,
                "nombre": empresa_paciente[0].empresa.nombre,
                "direccion": empresa_paciente[0].empresa.direccion,
                "cuit": empresa_paciente[0].empresa.cuit,
                "ultimo_recibo_de_sueldo": empresa_paciente[0].ultimo_recibo_de_sueldo.strftime('%d/%m/%Y'),
                "empresa_paciente": empresa_paciente[0].id,
            }
        else:
            empresa = {
                "encontrado": False,
            }
        data = {"paciente_id": paciente.id,
                "nombre": str(paciente.apellidos + ', ' + paciente.nombres),
                "dni": paciente.numero_documento,
                "encontrado": True,
                "empresa": empresa
                }
    else:
        data = {"encontrado": False}
    return JsonResponse(data, status=200)


def DatosPaciente(request, paciente_id):
    if Paciente.objects.filter(id=paciente_id).exists():
        paciente = Paciente.objects.get(id=paciente_id)
        data = {"paciente_id": paciente.id,
                "nombre": str(paciente.apellidos + ', ' + paciente.nombres),
                "dni": paciente.numero_documento
                }
        return JsonResponse(data, status=200)


def DatosPacienteEmpresa(request, empresa_paciente_id):
    if EmpresaPaciente.objects.filter(id=empresa_paciente_id).exists():
        paciente = EmpresaPaciente.objects.get(id=empresa_paciente_id)
        data = {"paciente_id": paciente.id,
                "nombre": str(paciente.apellidos + ', ' + paciente.nombres),
                "dni": paciente.numero_documento
                }
        return JsonResponse(data, status=200)
