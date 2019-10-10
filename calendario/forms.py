from datetime import timedelta
from django import forms
from tempus_dominus.widgets import DateTimePicker
from calendario.models import Turno


class FeedForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class TurnoForm(forms.ModelForm):
    bulk = forms.BooleanField(required=False)
    duration = forms.IntegerField(initial=10)

    def save(self, *args, **kwargs):
        if not self.cleaned_data['bulk']:
            return [super().save(*args, **kwargs)]

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
