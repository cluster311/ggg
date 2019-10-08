from django import forms
from calendario.models import Turno


class FeedForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'
