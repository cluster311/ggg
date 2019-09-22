from django.db import models
from model_utils import Choices
from address.models import AddressField
from django.utils.timezone import now


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"

    def __str__(self):
        return self.nombre


class CarpetaFamiliar(models.Model):
    OPCIONES_TIPO_FAMILIA = Choices(
        ('nuclear', 'Nuclear'),
        ('nuclear_ampliada', 'Nuclear Ampliada'),
        ('binuclear', 'Binuclear'),
        ('monoparental', 'Monoparental'),
        ('extensa','Extensa'),
        ('unipersonal','Unipersonal'),
        ('equivalentes', 'Equivalentes Familiares')
    )
    direccion = AddressField(null=True, on_delete=models.SET_NULL)
    tipo_familia = models.CharField(max_length=50, choices=OPCIONES_TIPO_FAMILIA)
    apellido_principal = models.CharField(max_length=100)

    def __str__(self):
        return 'Familia {0.apellido_principal} ({0.direccion})'.format(self)

    @property
    def jefe_familia(self):
        try:
            return self.miembros.filter(jefe_familia=True)[0]
        except IndexError:
            return None

    class Meta:
        verbose_name = "Carpeta familiar"
        verbose_name_plural = "Carpetas familiares"


class Paciente(models.Model):
    VINCULO_TYPE = Choices(
        ('Padre','Padre'),
        ('Hijo/a','Hijo/a'),
        ('Madre','Madre'),
        ('Abuelo/a','Abuelo/a'),
        ('Primo/a', 'Primo/a'),
        ('Nuera/Yerno', 'Nuera/Yerno'),
        ('Nieto/a', 'Nieto/a'),
        ('Cuñado/a', 'Cuñado/a'),
        ('Concuñado/a', 'Concuñado/a'),
        ('Tio/a', 'Tio/a'),
        ('Sobrino/a', 'Sobrino/a'),
        ('Esposo/a', 'Esposo/a'),
    )
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

    carpeta_familiar = models.ForeignKey('CarpetaFamiliar', null=True, related_name='miembros', on_delete=models.SET_NULL)
    nombres = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    sexo = models.CharField(max_length=20, choices=Choices('masculino', 'femenino', 'otro'))
    fecha_nacimiento = models.DateField()
    tipo_documento = models.CharField(max_length=20, choices=Choices('DNI', 'LC', 'LE', 'PASAPORTE', 'OTRO'))
    numero_documento = models.CharField(max_length=30, null=True, blank=True, help_text='Deje en blanco si está indocumentado')
    nacionalidad = models.CharField(max_length=50, choices=NACIONALIDAD_CHOICES)
    vinculo = models.CharField(max_length=50, null=True, choices=VINCULO_TYPE, help_text='Relación parental relativa a jefe de familia')
    es_jefe_familia = models.BooleanField(default=False)
    grupo_sanguineo = models.CharField(max_length=20, null=True, choices=Choices('0-', '0+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'))

    telefono = models.CharField(max_length=50, null=True, blank=True)
    obra_social = models.ForeignKey('ObraSocial', null=True, blank=True, on_delete=models.SET_NULL)
    observaciones = models.TextField()


    @property
    def edad(self):
        return (now().date() - self.fecha_nacimiento).days / 365

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f'{self.apellido}, {self.nombres}'
    