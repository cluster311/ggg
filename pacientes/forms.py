from dal import autocomplete
from django import forms
from cie10_django.models import CIE10
from pacientes.models import Consulta, Paciente


class ConsultaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(url='paciente-autocomplete')
    )
    codigo = forms.ModelChoiceField(
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='cie10-autocomplete')
    )

    class Meta:
        model = Consulta
        fields = ('__all__')


class PacienteForm(forms.ModelForm):
    numero_documento = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(url='paciente-autocomplete')
    )

    class Meta:
        model = Paciente
        fields = ('__all__')
