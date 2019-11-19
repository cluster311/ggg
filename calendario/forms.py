import pytz
from dal import autocomplete
from datetime import datetime, timedelta, time
from django import forms
from django.db.models import Count
from django.conf import settings
from calendario.models import Turno
from calendario.widgets import DateTimePicker
from profesionales.models import Profesional
from pacientes.models import Paciente
from obras_sociales.models import ObraSocialPaciente, ObraSocial
from centros_de_salud.models import ProfesionalesEnServicio, Servicio
import logging
logger = logging.getLogger(__name__)


LOCAL_TZ = pytz.timezone(settings.TIME_ZONE)


class FeedForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class TurnoForm(forms.ModelForm):
    bulk = forms.BooleanField(required=False, label='En masa')
    duration = forms.IntegerField(initial=10, label='Duración')
    delete = forms.BooleanField(required=False, initial=False)

    profesional = forms.ModelChoiceField(
        label='Profesional en el servicio',
        #TODO este qs tarde varios segundos en cargar cuando es muy grande
        # queryset=Profesional.objects.all(),
        # dejar solo los profesionales que tienen al menos un servicio
        queryset=Profesional.objects.annotate(num_servicios=Count('servicios')).filter(num_servicios__gte=1),
        
    )

    servicio = forms.ModelChoiceField(
        label='Servicios',
        queryset=Servicio.objects.all(),
        widget=autocomplete.ModelSelect2(),
    )
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Add custom bootstrap classes to form fields' CSS.
        for field in self.fields.keys():
            classes_to_ad = 'form-control'
            if field == 'estado':
                classes_to_ad += ' custom-select'
            self.fields[field].widget.attrs.update({'class': classes_to_ad})
        
        if user is not None:
            csp = user.centros_de_salud_permitidos.all()
            centros_de_salud_permitidos = [c.centro_de_salud for c in csp]
            qs = Servicio.objects.filter(centro__in=centros_de_salud_permitidos)
            self.fields['servicio'].queryset = qs

    def clean(self, *args, **kwargs):

        cleaned_data = super().clean(*args, **kwargs)
        logger.info(f'Cleaning turno form {cleaned_data}')
        
        # ver que el profesional este en el servicio
        servicio = cleaned_data['servicio']
        profesional = cleaned_data['profesional']
        q = ProfesionalesEnServicio.objects.filter(servicio=servicio,
                                                   profesional=profesional)
        
        if q.count() == 0:
            error = {'profesional': ["El profesional no esta asignado al servicio"]}
            logger.error(error)
            raise forms.ValidationError(error)
            
        else:
            if q[0].estado != ProfesionalesEnServicio.EST_ACTIVO:
                error = {'profesional': ["El profesional no esta activado asignado al servicio"]}
                logger.error(error)
                raise forms.ValidationError(error)

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

    def update(self, data, *args, **kwargs):
        paciente = Paciente.objects.filter(numero_documento=data['paciente']).first()
        if paciente is None:
            save, result = Paciente.create_from_sisa(data['paciente'])
            if not save and ('nombres' in data and 'apellidos' in data):
                #Se esta inicializando por medio de la gestion de un administrativo
                paciente = Paciente.objects.create(
                    numero_documento=data['paciente'],
                    nombres=data['nombres'],
                    apellidos=data['apellidos'],
                )
                ObraSocialPaciente.objects.create(
                    data_source=settings.SOURCE_OSS_SISA,
                    paciente=paciente,
                    obra_social_updated=datetime.now(),
                    obra_social=ObraSocial.objects.get(pk=data['oss']),
                    numero_afiliado=data['numero-afiliado'] if 'numero-afiliado' in data else None
                )
                self.instance.paciente = paciente
                self.instance.solicitante = data['solicitante']
                self.instance.estado = Turno.ASIGNADO
                self.instance.save()
                return True, self.instance
            else:
                return save, result
        else:
            self.instance.paciente = paciente
            self.instance.solicitante = data['solicitante']
            self.instance.estado = Turno.ASIGNADO
            self.instance.save()
            return True, self.instance
    
    def change_state(self, data, *args, **kwargs):
        try:
            new_state = int(data['state'])
            if new_state == Turno.ESPERANDO_EN_SALA:
                if self.instance.profesional is None:
                    error = {'profesional': 'El turno deberia tener un profesional asignado'}
                    return False, error
                elif self.instance.paciente is None:
                    error = {'paciente': 'El turno deberia tener un paciente asignado'}
                    return False, error
            if new_state >= 0 and new_state < len(Turno.OPCIONES_ESTADO):
                self.instance.estado = int(data['state'])
                self.instance.save()
                return True, self.instance
            else:
                error = {'state': 'No es un estado valido'}
                return False, error
        except Exception as e:
            error = {'state': f'Error al cambiar el estado: {e}'}
            return False, error

    class Meta:
        model = Turno
        fields = ['inicio', 'fin', 'servicio', 'profesional', 'bulk', 'duration']
        widgets = {
            'inicio': DateTimePicker(),
            'fin': DateTimePicker(),
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
