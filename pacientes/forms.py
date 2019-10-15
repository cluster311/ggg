from dal import autocomplete
from django import forms
from cie10_django.models import CIE10
from pacientes.models import Consulta


class ConsultaForm(forms.ModelForm):
    codigo = forms.ModelChoiceField(
        queryset=CIE10.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='cie10-autocomplete')
    )

    class Meta:
        model = Consulta
        fields = ('__all__')