from django.contrib.gis.db import models
from address.models import AddressField
from tinymce.models import HTMLField


class Institucion(models.Model):
    """Las instituciones son las administradoras finales de los centros
    de salud.
    """
    nombre = models.CharField(max_length=290)

    def __str__(self):
        return self.nombre


class CentroDeSalud(models.Model):
    nombre = models.CharField(max_length=290)
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='centros'
    )
    codigo_hpgd = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text=(
            'Código de Hospital Público de Gestión Descentralizada. '
            'Requerido para recupero'
        )
    )

    descripcion = HTMLField(null=True, blank=True)
    horario_de_atencion = models.TextField(null=True, blank=True)
    direccion = AddressField(null=True, blank=True, on_delete=models.SET_NULL)
    telefonos = models.TextField(null=True, blank=True)

    ubicacion = models.PointField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Centro de Salud'
        verbose_name_plural = 'Centros de Salud'
        permissions = [
            (
                "can_view_tablero",
                "Ver tableros de comandos",
            )
        ]


class Especialidad(models.Model):
    """
    obstetricia, dermatología, etc
    """
    nombre = models.CharField(max_length=290)
    tiempo_predeterminado_turno = models.PositiveIntegerField(default=15)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """
    este modelo representa una especialidad en un determinado centro de salud
    """
    centro = models.ForeignKey(CentroDeSalud, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.especialidad} - {self.centro}'


class ProfesionalesEnServicio(models.Model):
    """ cada uno de los profesionales activos en un servicio particular """
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='profesionales')
    profesional = models.ForeignKey('profesionales.Profesional', on_delete=models.CASCADE, related_name='servicios')

    EST_INACTIVO = 100
    EST_ACTIVO = 200
    estados = ((EST_INACTIVO, 'Inactivo'),
               (EST_ACTIVO, 'Activo'))

    estado = models.PositiveIntegerField(choices=estados, default=EST_ACTIVO)

    def __str__(self):
        return '{self.profesional} en {self.servicio}'