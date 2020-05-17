from address.forms import AddressField, AddressWidget
from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from cie10_django.models import CIE10
from pacientes.models import (Consulta, Paciente, Receta, Derivacion,
                              CarpetaFamiliar)
from profesionales.models import Profesional
from recupero.models import Prestacion, TipoPrestacion
from centros_de_salud.models import CentroDeSalud, Servicio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import logging
logger = logging.getLogger(__name__)


class RecetaForm(forms.ModelForm):

    class Meta:
        model = Receta
        fields = ('medicamento', 'posologia', 'observaciones')
        widgets = {
          'posologia': forms.Textarea(attrs={'rows':2, 'cols':15}),
          'observaciones': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }


class DerivacionForm(forms.ModelForm):

    class Meta:
        model = Derivacion
        fields = ('especialidad', 'observaciones')
        widgets = {
          'observaciones': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }


class PrestacionForm(forms.ModelForm):

    tipo = forms.ModelChoiceField(
        queryset=TipoPrestacion.objects.all(),
        label='Práctica',
        widget=autocomplete.ModelSelect2(
            url="tipo_prestacion-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    class Meta:
        model = Prestacion
        fields = ('tipo', 'cantidad', 'observaciones')
        widgets = {
          'observaciones': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }


RecetaFormset = inlineformset_factory(Consulta, Receta, form=RecetaForm, extra=1)
PrestacionFormset = inlineformset_factory(Consulta, Prestacion, form=PrestacionForm, extra=1)
DerivacionFormset = inlineformset_factory(Consulta, Derivacion, form=DerivacionForm, extra=1)


class EvolucionForm(forms.ModelForm):
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
    indicaciones = forms.CharField(
        required=False,
        label='Indicaciones adicionales',
        widget=forms.Textarea(attrs={'rows': 2})
    )

    class Meta:
        model = Consulta
        fields = ('motivo_de_la_consulta', 'codigo_cie_principal',
                  'codigos_cie_secundarios',
                  'evolucion', 'indicaciones')
        widgets = {
          'motivo_de_la_consulta': forms.Textarea(attrs={'rows': 3}),
          'evolucion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Form update basado en lib crispy
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Actualizar"))

        if user is not None:
            csp = user.centros_de_salud_permitidos.all()
            permitidos = [c.centro_de_salud.id for c in csp]
            qs = CentroDeSalud.objects.filter(pk__in=permitidos)
            self.fields['centro_de_salud'].queryset = qs


class ConsultaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="paciente-autocomplete",
            attrs={
                "data-placeholder": "Ingrese nombre o número de documento",
                "data-minimum-input-length": 3,
            },
        ),
    )
    profesional = forms.ModelChoiceField(
        required=False,
        queryset=Profesional.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profesional-autocomplete",
            attrs={
                "data-placeholder": "Ingrese número de documento",
                "data-minimum-input-length": 3,
            },
        ),
    )
    centro_de_salud = forms.ModelChoiceField(
        required=False,
        queryset=CentroDeSalud.objects.all(),
        )
    codigo_cie_principal = forms.ModelChoiceField(
        required=False,
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    codigos_cie_secundarios = forms.ModelMultipleChoiceField(
        required=False,
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    class Meta:
        model = Consulta
        fields = ('paciente', 'profesional', 'centro_de_salud',
                  'especialidad', 'codigo_cie_principal',
                  'codigos_cie_secundarios',
                  'evolucion', 'indicaciones')
        widgets = {
          'evolucion': forms.Textarea(attrs={'rows':3}),
          'indicaciones': forms.Textarea(attrs={'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Form update basado en lib crispy
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Actualizar"))

        if user is not None:
            csp = user.centros_de_salud_permitidos.all()
            permitidos = [c.centro_de_salud.id for c in csp]
            qs = CentroDeSalud.objects.filter(pk__in=permitidos)
            self.fields['centro_de_salud'].queryset = qs


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


class CarpetaFamiliarForm(forms.ModelForm):

    class Meta:
        model = CarpetaFamiliar
        fields = [
                  "direccion",
                  "apellido_principal",
                  "tipo_familia"
                  ]
        # field_classes = {
        #     'direccion': AddressField,
        # }
        # widgets = {
        #   'direccion': AddressWidget,
        # }
        help_texts = {
            'direccion': _("Ingrese calle, número y ciudad. Ejemplo: Avenida "
                           "Colón 4230, Córdoba"),
            'apellido_principal': _("Apellido identificatorio de la familia.")
        }
