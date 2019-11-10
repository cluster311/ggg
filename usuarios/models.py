from django.db import models
from django.contrib.auth.models import User


class UsuarioEnCentroDeSalud(models.Model):
    """ Permisos de los usuarios administrativos sobre los centros de salud
        Cada usuario tendra sus permisos pero solo sobre una lista de centros de salud
        """

    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='centros_de_salud_permitidos')
    centro_de_salud = models.ForeignKey('centros_de_salud.CentroDeSalud',
                                        on_delete=models.CASCADE,
                                        related_name='usuarios_permitidos')
    
    EST_INACTIVO = 100
    EST_ACTIVO = 200
    estados = ((EST_INACTIVO, 'Inactivo'),
               (EST_ACTIVO, 'Activo'))

    estado = models.PositiveIntegerField(choices=estados, default=EST_ACTIVO)
    
    def __str__(self):
        return f'{self.usuario} en {self.centro_de_salud}'
