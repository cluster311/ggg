from dal import autocomplete
from cie10_django.models import CIE10
from django.shortcuts import render, render_to_response, redirect

from pacientes.models import Paciente, CarpetaFamiliar
from profesionales.models import Profesional
from centros_de_salud.models import (CentroDeSalud, ProfesionalesEnServicio,
                                     Servicio)
from recupero.models import TipoPrestacion
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)


class CIE10Autocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autompletado para códigos de diagnósticos.
    """

    def get_result_label(self, item):
        return f"{item.code} - {item.description}"

    def get_selected_result_label(self, item):
        return item.code

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CIE10.objects.none()

        qs = CIE10.objects.all()

        if self.q:
            qs = qs.filter(Q(code__icontains=self.q) |
                           Q(description__icontains=self.q)
                           )

        return qs.order_by("code")


class PacienteAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autompletado para pacientes.
    """

    def get_queryset(self):
        if not self.request.user.has_perm('pacientes.view_paciente'):
            return Paciente.objects.none()

        qs = Paciente.objects.all()

        if self.q:
            qs = qs.filter(Q(numero_documento__icontains=self.q) |
                           Q(nombres__icontains=self.q) |
                           Q(apellidos__icontains=self.q)
                           )

        return qs.order_by("apellidos", "nombres")[:5]


class ProfesionalAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autocompletado para profesionales.
    """

    def get_queryset(self):
        if not self.request.user.has_perm('profesionales.view_profesional'):
            return Profesional.objects.none()

        qs = Profesional.objects.all()

        if 'servicio_id' in self.kwargs:
            si = self.kwargs['servicio_id']
            qs = qs.filter(servicios__servicio=si, servicios__estado=ProfesionalesEnServicio.EST_ACTIVO)
            logger.info(f'Profesionales por servicio {si}')

        if self.q:
            qs = qs.filter(Q(numero_documento__icontains=self.q) |
                           Q(nombres__icontains=self.q) |
                           Q(apellidos__icontains=self.q)
                           )

        return qs.order_by("apellidos", "nombres")[:5]


class CentroDeSaludAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autompletado para Centros de Salud.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CentroDeSalud.objects.none()

        qs = CentroDeSalud.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs.order_by("nombre")[:5]


class TipoPrestacionAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autocompletado para tipos de prestaciones.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TipoPrestacion.objects.none()

        qs = TipoPrestacion.objects.all()

        if self.q:
            qs = qs.filter(Q(codigo__icontains=self.q) |
                           Q(nombre__icontains=self.q) |
                           Q(descripcion__icontains=self.q)
                           )

        return qs.order_by("nombre")[:5]


class CarpetaFamiliarAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autompletado para pacientes.
    """

    def get_result_label(self, item):
        return f"{item.apellido_principal} - {item.direccion}"

    def get_selected_result_label(self, item):
        return item.apellido_principal

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CarpetaFamiliar.objects.none()

        qs = CarpetaFamiliar.objects.all()

        if self.q:
            qs = qs.filter(Q(apellido_principal__icontains=self.q) |
                           Q(direccion__icontains=self.q)
                           )

        return qs.order_by("apellido_principal")[:10]


class ServicioAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autocompletado para tipos de prestaciones.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Servicio.objects.none()

        # if user is not None:
        #     csp = user.centros_de_salud_permitidos.all()
        #     centros_de_salud_permitidos = [c.centro_de_salud for c in csp]
        #     qs = Servicio.objects.filter(centro__in=centros_de_salud_permitidos)
        #     self.fields['servicio'].queryset = qs

        qs = Servicio.objects.all()

        if self.q:
            qs = qs.filter(especialidad__nombre__icontains=self.q)

        return qs


def handler403(request, exception):
    if not request.user.is_anonymous:
        response = render_to_response("errors/403.html")
        response.status_code = 403
        return response
    else:
        return redirect('../../accounts/login/?next='+request.get_full_path(),)


