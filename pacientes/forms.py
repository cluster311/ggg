from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from cie10_django.models import CIE10
from pacientes.models import Consulta, Paciente, Receta, Derivacion
from profesionales.models import Profesional
from recupero.models import Prestacion, TipoPrestacion
from centros_de_salud.models import CentroDeSalud
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
    centro_de_salud = forms.ModelChoiceField(
        queryset=CentroDeSalud.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="centro_de_salud-autocomplete",
            attrs={
                "data-placeholder": "Ingrese número de documento",
                "data-minimum-input-length": 3,
            },
        ),
    )
    codigo_cie_principal = forms.ModelChoiceField(
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    codigos_cie_secundarios = forms.ModelMultipleChoiceField(
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="cie10-autocomplete",
            attrs={"data-placeholder": "Ingrese código o descripción"}
        ),
    )

    class Meta:
        model = Consulta
        fields = ('paciente', 'profesional', 'centro_de_salud',
                  'codigo_cie_principal',
                  'codigos_cie_secundarios',
                  'diagnostico', 'indicaciones')
        widgets = {
          'diagnostico': forms.Textarea(attrs={'rows':3}),
          'indicaciones': forms.Textarea(attrs={'rows':3}),
        }

    def form_valid(self, form):
        context = self.get_context_data()
        
        rs = context["recetas_frm"]
        ds = context["derivaciones_frm"]
        ps = context["prestaciones_frm"]

        self.object = form.save()
        
        if rs.is_valid():
            rs.instance = self.object
            rs.save()
        
        if ds.is_valid():
            ds.instance = self.object
            ds.save()
        
        if ps.is_valid():
            ps.instance = self.object
            ps.save()
        
        return super().form_valid(form)

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
