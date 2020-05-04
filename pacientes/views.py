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
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.conf import settings
from .models import Consulta, CarpetaFamiliar
from especialidades.models import MedidasAnexasEspecialidad, MedidaAnexaEnConsulta
from especialidades.forms import MedidaAnexaEnConsultaForm, MedidaAnexaEnConsultaFormset
from calendario.models import Turno
from .forms import (EvolucionForm, ConsultaForm,
                   RecetaFormset, DerivacionFormset, 
                   PrestacionFormset, CarpetaFamiliarForm)
from crispy_forms.utils import render_crispy_form
import logging
logger = logging.getLogger(__name__)


class ConsultaListView(PermissionRequiredMixin, ListView):
    """
    Lista de consultas de un paciente para la interfaz del profesional.
    """

    model = Consulta
    permission_required = ("pacientes.view_consulta",)
    template_name = "pacientes/consulta_listview.html"

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
            consultas_previas = Consulta.objects.filter(
                paciente=instance.paciente
                ).exclude(pk=instance.pk).order_by('-created')
            context['consultas_previas'] = consultas_previas
        
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
    permission_required = ("calendario.can_gestionar_turnos",)

    # descomentar si queremos un boton con link arriba a la derecha
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Carpeta Familiar'
    #     context['subtitle'] = 'Nueva Carpeta Familiar'
    #     context['title_url'] = 'profesionales.lista'
    #     return context

    def get_success_url(self):
        return reverse(
            "calendario.gestion_turno"
        )
