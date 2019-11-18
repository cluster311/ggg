from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from pacientes.models import Consulta
import logging
logger = logging.getLogger(__name__)


class Turno(models.Model):
    DISPONIBLE = 0
    ASIGNADO = 1
    ESPERANDO_EN_SALA = 2
    ATENDIDO = 3
    CANCELADO_PACIENTE = 4
    CANCELADO_ESTABLECIMIENTO = 5

    OPCIONES_ESTADO = (
        (DISPONIBLE, 'Disponible'),
        (ASIGNADO, 'Asignado'),
        (ESPERANDO_EN_SALA, 'Esperando en sala'),
        (ATENDIDO, 'Atendido'),
        (CANCELADO_PACIENTE, 'Cancelado por el paciente'),
        (CANCELADO_ESTABLECIMIENTO, 'Cancelado por el establecimiento')
    )

    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    servicio = models.ForeignKey(
        'centros_de_salud.Servicio',
        on_delete=models.CASCADE
    )
    profesional = models.ForeignKey(
        'profesionales.Profesional',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    paciente = models.ForeignKey(
        'pacientes.Paciente',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    solicitante = models.ForeignKey(
        User, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL
    )
    estado = models.IntegerField(choices=OPCIONES_ESTADO, default=DISPONIBLE)

    class Meta:
        permissions = [
            (
                "can_schedule_turno",
                "Puede agendar un turno",
            ),
            (
                "can_view_misturnos",
                "Puede ver Mis Turnos"
            ),
            (
                "can_cancel_turno",
                "Puede cancelar sus turnos"
            ),
            (
                "can_gestionar_turnos",
                "Puede gestionar turnos"
            ),
            
        ]

    def __str__(self):
        return f'{self.servicio.especialidad}'

    def as_json(self):
        json = {
            'inicio': datetime.strftime(self.inicio, '%d/%m/%Y %H:%M'),
            'servicio': self.servicio.especialidad.nombre,
            'estado': self.get_estado_display(),
        }
        if self.paciente is not None:
            json['paciente'] = '{}, {}'.format(
                self.paciente.apellidos, self.paciente.nombres)
        if self.profesional is not None:
            json['profesional'] = '{}, {}'.format(
                self.profesional.apellidos, self.profesional.nombres)
        return json
        
    def save(self, *args, **kwargs):
        """ ver si corresponde crear una consulta """
        super().save(*args, **kwargs)
        
        if self.estado in [self.CANCELADO_PACIENTE, self.CANCELADO_ESTABLECIMIENTO]:
            logger.info('Grabando Turno en estado cacelado')
            if hasattr(self, 'consulta'):
                # TODO ¿debería eliminar la consulta?
                logger.info(f'Eliminando consulta {self.consulta.id} por cancelación de turno')
                self.consulta.delete()
            else:
                logger.info(f'No existía una consulta asociada')

        if self.estado in [self.ESPERANDO_EN_SALA, self.ASIGNADO]:
            consulta, created = Consulta.objects.get_or_create(
                turno=self, paciente=self.paciente
            )
            if created:
                logger.info(f'Consulta derivada de Turno creada {consulta.id}')
            else:
                logger.info(f'Consulta derivada de Turno ya existía {consulta.id}')
            
            consulta.profesional = self.profesional
            consulta.centro_de_salud = self.servicio.centro
            consulta.especialidad = self.servicio.especialidad

            consulta.save()