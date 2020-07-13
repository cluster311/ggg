from cie10_django.models import CIE10
from django import forms
from django.forms import inlineformset_factory
from calendario.widgets import DateTimePicker
from centros_de_salud.models import CentroDeSalud, Especialidad
from obras_sociales.models import ObraSocial
from pacientes.models import Paciente
from dal import autocomplete

from profesionales.models import Profesional
from recupero.models import Factura, FacturaPrestacion, TipoPrestacion


class FacturaPrestacionForm(forms.ModelForm):

    class Meta:
        model = FacturaPrestacion
        fields = ('tipo', 'cantidad', 'observaciones',)
        widgets = {'observaciones':  forms.Textarea(attrs={'rows': 2, 'cols': 10}),
                   }


class FacturaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        label='Paciente',
        required=False,
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="paciente-autocomplete",
            attrs={"data-placeholder": "Ingrese nombre, apellido o documento"}
        ),
    )
    obra_social = forms.ModelChoiceField(
        label='Obra Social',
        required=False,
        queryset=ObraSocial.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="obra-social-autocomplete",
            forward=['paciente'],
            attrs={"data-placeholder": "Seleccione una Obra social"}
        ),
    )
    centro_de_salud = forms.ModelChoiceField(
        label='Centro de Salud',
        required=False,
        queryset=CentroDeSalud.objects.all(),
        empty_label="Seleccione un valor",
    )
    especialidad = forms.ModelChoiceField(
        label='Especialidad',
        required=False,
        queryset=Especialidad.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="especialidad-autocomplete",
            forward=['centro_de_salud'],
            attrs={"data-placeholder": "Seleccione una Especialidad"}
        ),
    )
    profesional = forms.ModelChoiceField(
        label='Profesional',
        required=False,
        queryset=Profesional.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profesional-autocomplete",
            forward=['especialidad', 'centro_de_salud'],
            attrs={"data-placeholder": "Seleccione un Profesional"}
        ),
    )
    codigo_cie_principal = forms.ModelChoiceField(
        label='Código CIE10 principal',
        required=False,
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    codigos_cie_secundarios = forms.ModelMultipleChoiceField(
        label='Códigos CIE10 secundarios',
        required=False,
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            csp = user.centros_de_salud_permitidos.all()
            permitidos = [c.centro_de_salud.id for c in csp]
            self.fields['centro_de_salud'].queryset = CentroDeSalud.objects.filter(pk__in=permitidos)

    class Meta:
        model = Factura
        fields = ('fecha_atencion',
                  'paciente',
                  'obra_social',
                  'profesional',
                  'especialidad',
                  'centro_de_salud', 'fecha_atencion',
                  'codigo_cie_principal',
                  'codigos_cie_secundarios',
                   )
        widgets = {'fecha_atencion': DateTimePicker()}


FacturaPrestacionFormSet = inlineformset_factory(Factura, FacturaPrestacion, form=FacturaPrestacionForm, extra=1)
