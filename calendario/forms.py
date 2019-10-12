import pytz
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
    id = forms.IntegerField(required=False)
    delete = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            classes_to_ad = 'form-control'
            if isinstance(self.fields[field].widget, forms.widgets.Select):
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
        if self.cleaned_data['id']:
            appointment = Turno.objects.get(id=self.cleaned_data['id'])

            if self.cleaned_data['delete']:
                appointment.delete()
                return ()

            for field in (f for f in self.cleaned_data if f != 'id'):
                setattr(appointment, field, self.cleaned_data[field])
            appointment.save()
            appointment = Turno.objects.get(pk=appointment.pk)
            print(appointment.inicio, appointment.inicio.tzinfo)
            return (appointment, )

        if not self.cleaned_data['bulk']:
            return (super().save(*args, **kwargs), )

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
                if k not in ('bulk', 'duration', 'inicio', 'fin')
            }
            appointment_data['inicio'] = current_time
            appointment_data['fin'] = end_time
            appointments.append(Turno.objects.create(**appointment_data))
            current_time = end_time
        return appointments

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
