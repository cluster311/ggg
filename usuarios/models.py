from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from model_utils.models import TimeStampedModel


class UsuarioEnCentroDeSalud(TimeStampedModel):
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
    elegido = models.BooleanField(default=False, help_text='Solo uno puede estar elegido en cada momento')

    def elegir(self):
        elegido = UsuarioEnCentroDeSalud.objects.filter(usuario=self.usuario, elegido=True).first()
        if elegido == self:
            return False
        UsuarioEnCentroDeSalud.objects.filter(usuario=self.usuario).update(elegido=False)
        self.elegido = True
        self.save()
        return True
    
    def __str__(self):
        return f'{self.usuario} en {self.centro_de_salud}'
    
    def save(self, *args, **kwargs):
        """ cuando un usuario es asignado a un 
            centro de salud es de hecho un 
            usuario administrativo """
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name=settings.GRUPO_ADMIN)
        group.user_set.add(self.usuario)
