from dal import autocomplete
from django import forms
from cie10_django.models import CIE10
from pacientes.models import Consulta, Paciente


class ConsultaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(url='paciente-autocomplete',
                                         attrs={
                                                'data-placeholder': 'Ingrese número de documento',
                                                'data-minimum-input-length': 3,
                                        },
        )
    )
    codigo = forms.ModelMultipleChoiceField(
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='cie10-autocomplete',
                                                 attrs={
                                                        'data-placeholder': 'Ejemplo: A00',
                                                },
        )
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
