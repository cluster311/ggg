from dal import autocomplete
from django import forms
from cie10_django.models import CIE10
from pacientes.models import Consulta, Paciente
from profesionales.models import Profesional
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ConsultaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="paciente-autocomplete",
            attrs={
                "data-placeholder": "Ingrese número de documento",
                "data-minimum-input-length": 3,
            },
        ),
    )
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profesional-autocomplete",
            attrs={
                "data-placeholder": "Ingrese número de documento",
                "data-minimum-input-length": 3,
            },
        ),
    )
    codigo_cie_principal = forms.ModelMultipleChoiceField(
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    class Meta:
        model = Consulta
        fields = ('paciente', 'profesional', 'codigo_cie_principal',
                  'diagnostico', 'indicaciones')

    def __init__(self, *args, **kwargs):
        """
        Form update basado en lib crispy
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Actualizar"))


class PacienteForm(forms.ModelForm):
    numero_documento = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="paciente-autocomplete",
            attrs={
                "data-placeholder": "Ingrese número de documento",
                "data-minimum-input-length": 3,
            },
        ),
    )

    class Meta:
        model = Paciente
        fields = ("numero_documento",)
