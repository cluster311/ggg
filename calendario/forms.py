from django import forms
from tempus_dominus.widgets import DateTimePicker
from calendario.models import Turno


class FeedForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'
        widgets = {
            'inicio': DateTimePicker(
                options={
                    'icons': {
                        'time': 'fa fa-clock',
                    }
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'input_toggle': False,
                    'icon_toggle': True,
                }
            ),
            'fin': DateTimePicker(
                options={
                    'icons': {
                        'time': 'fa fa-clock',
                    }
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'input_toggle': False,
                    'icon_toggle': True,
                }
            )
        }
