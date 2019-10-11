from dal import autocomplete
from cie10_django.models import CIE10
from pacientes.models import Paciente


class CIE10Autocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autompletado para códigos de diagnósticos.
    """
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CIE10.objects.none()

        qs = CIE10.objects.all()

        if self.q:
            qs = qs.filter(code__istartswith=self.q)

        return qs.order_by('code')


class PacienteAutocomplete(autocomplete.Select2QuerySetView):
    """
    Base de autompletado para pacientes.
    """
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Paciente.objects.none()

        qs = Paciente.objects.all()

        if self.q:
            qs = qs.filter(numero_documento__istartswith=self.q)

        return qs