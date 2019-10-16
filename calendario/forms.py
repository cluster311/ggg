import pytz
from dal import autocomplete
from datetime import timedelta
from django import forms
from tempus_dominus.widgets import DateTimePicker
from calendario.models import Turno


LOCAL_TZ = pytz.timezone('America/Argentina/Buenos_Aires')


class FeedForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class TurnoForm(forms.ModelForm):
    bulk = forms.BooleanField(required=False, label='En masa')
    duration = forms.IntegerField(initial=10, label='Duración')
    delete = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom bootstrap classes to form fields' CSS.
        for field in self.fields.keys():
            classes_to_ad = 'form-control'
            if field == 'estado':
                classes_to_ad += ' custom-select'
            self.fields[field].widget.attrs.update({'class': classes_to_ad})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        for field in ('inicio', 'fin'):
            cleaned_data[field] = LOCAL_TZ.localize(
                cleaned_data[field].replace(tzinfo=None)
            )
        return cleaned_data

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
            ),
            'servicio': autocomplete.ModelSelect2(),
            'profesional': autocomplete.ModelSelect2(),
            'paciente': autocomplete.ModelSelect2(),
        }


class BulkTurnoForm(TurnoForm):
    def save(self, *args, **kwargs):
        appointments = []
        current_time = self.cleaned_data['inicio']
        while current_time < self.cleaned_data['fin']:
            end_time = min([
                current_time + timedelta(
                    minutes=self.cleaned_data['duration']
                ),
                self.cleaned_data['fin']
            ])
            appointment_data = {
                k: v for k, v in self.cleaned_data.items()
                if k not in ('bulk', 'duration', 'inicio', 'fin', 'delete')
            }
            appointment_data['inicio'] = current_time
            appointment_data['fin'] = end_time
            appointments.append(Turno.objects.create(**appointment_data))
            current_time = end_time
        return appointments
