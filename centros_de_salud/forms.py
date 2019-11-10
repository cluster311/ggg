from dal import autocomplete
from django import forms
from .models import ProfesionalesEnServicio
from profesionales.models import Profesional


class ProfesionalesEnServicioForm(forms.ModelForm):

    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profesional-autocomplete",
            attrs={"data-placeholder": "Ingrese nombre o dni del profesional"}
        ),
    )

    class Meta:
        model = ProfesionalesEnServicio
        fields = ['servicio', 'profesional', 'estado']
