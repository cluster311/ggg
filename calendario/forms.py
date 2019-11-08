import pytz
from dal import autocomplete
from datetime import datetime, timedelta, time
from django import forms
from django.conf import settings
from calendario.models import Turno
from calendario.widgets import DateTimePicker


LOCAL_TZ = pytz.timezone(settings.TIME_ZONE)


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
    
    def save(self, *args, **kwargs):
        turno_date = self.cleaned_data['inicio']
        while turno_date < self.cleaned_data['fin']:
            turno_time = time(turno_date.hour, turno_date.minute)
            end_time = time(self.cleaned_data['fin'].hour, self.cleaned_data['fin'].minute)
            while turno_time < end_time:
                data = {
                    k: v for k, v in self.cleaned_data.items()
                    if k not in ('bulk', 'duration', 'inicio', 'fin', 'delete')
                }
                data['inicio'] = turno_date.replace(
                    hour=turno_time.hour, 
                    minute=turno_time.minute, 
                    second=turno_time.second
                )
                horas = int((turno_time.minute + self.cleaned_data['duration']) / 60)
                mins = (turno_time.minute + self.cleaned_data['duration']) % 60
                data['fin'] = turno_date.replace(
                    hour=turno_time.hour + horas, 
                    minute=mins
                )
                turno = Turno.objects.create(**data)
                turno_time = time(turno_time.hour + horas, mins)
            turno_date = turno_date + timedelta(days=1)
        return turno

    class Meta:
        model = Turno
        fields = ['inicio', 'fin', 'servicio', 'profesional', 'bulk', 'duration']
        widgets = {
            'inicio': DateTimePicker(),
            'fin': DateTimePicker(),
            'servicio': autocomplete.ModelSelect2(),
            'profesional': autocomplete.ModelSelect2(),
            # 'paciente': autocomplete.ModelSelect2(),
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
