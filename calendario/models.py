from django.db import models
from datetime import datetime


class Turno(models.Model):
    DISPONIBLE = 0
    ASIGNADO = 1
    ATENDIDO = 2
    CANCELADO_PACIENTE = 3
    CANCELADO_ESTABLECIMIENTO = 4

    OPCIONES_ESTADO = (
        (DISPONIBLE, 'Disponible'),
        (ASIGNADO, 'Asignado'),
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
    estado = models.IntegerField(choices=OPCIONES_ESTADO, default=DISPONIBLE)

    class Meta:
        permissions = [
            (
                "can_schedule_turno",
                "Puede agendar un turno",
            )
        ]

    def __str__(self):
        return f'{self.servicio.especialidad}'

    def as_json(self):
        json = {
            'inicio': datetime.strftime(self.inicio, '%d/%m/%Y %H:%M'),
            'servicio': self.servicio.especialidad.nombre,
            'paciente': '{}, {}'.format(
                self.paciente.apellidos, self.paciente.nombres)
        }
        if self.profesional is not None:
            json['profesional'] = '{}, {}'.format(
                self.profesional.apellidos, self.profesional.nombres)
        return json
