from django.db import models
from model_utils import Choices
from address.models import AddressField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class Persona(models.Model):
    NACIONALIDAD_CHOICES = Choices(
        'argentina',
        'boliviana',
        'brasilera',
        'chilena', 
        'colombiana', 
        'ecuatoriana',
        'paraguaya',
        'peruana',
        'uruguaya',
        'venezolana',
        'otra',
    )

    nombres = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    sexo = models.CharField(max_length=20,
                    choices=Choices('masculino', 'femenino', 'otro'))
    fecha_nacimiento = models.DateField()
    tipo_documento = models.CharField(max_length=20, default='DNI',
                        choices=Choices('DNI', 'LC', 'LE', 'PASAPORTE', 'OTRO'))
    numero_documento = models.CharField(max_length=30, null=True, blank=True, help_text='Deje en blanco si está indocumentado')
    nacionalidad = models.CharField(max_length=50, choices=NACIONALIDAD_CHOICES,
                    default=NACIONALIDAD_CHOICES.argentina)

    @property
    def edad(self):
        return (now().date() - self.fecha_nacimiento).days / 365

    class Meta:
        abstract = True

    def __str__(self):
        return '{}, {}'.format(self.apellido, self.nombres)
