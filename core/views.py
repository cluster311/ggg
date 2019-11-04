from dal import autocomplete
from cie10_django.models import CIE10
from pacientes.models import Paciente
from profesionales.models import Profesional
from centros_de_salud.models import CentroDeSalud
from django.db.models import Q


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