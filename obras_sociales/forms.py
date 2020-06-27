from django import forms
from calendario.widgets import DateTimePicker
from obras_sociales.models import ObraSocial, ObraSocialPaciente
from dal import autocomplete

from pacientes.models import Paciente


class ObraSocialPacienteCreatePopUp(forms.ModelForm):
    obra_social = forms.ModelChoiceField(
        label='Obra Social',
        required=False,
        queryset=ObraSocial.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="obra-social-all-autocomplete",
            attrs={"data-placeholder": "Seleccione una Obra social"}
        ),
    )
    paciente = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Paciente.objects.all(),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ObraSocialPaciente
        fields = ('paciente',
                  'obra_social',
                  'numero_afiliado',
                  'fecha_de_emision',
                  'fecha_de_vencimiento',
                   )
        widgets = {'fecha_de_emision': DateTimePicker(),
                   'fecha_de_vencimiento': DateTimePicker(),
                   }
