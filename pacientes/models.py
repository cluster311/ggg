from django.db import models
from core.models import Persona
from profesionales.models import Profesional
from model_utils import Choices
from address.models import AddressField
from django.contrib.contenttypes.fields import (GenericForeignKey,
    GenericRelation)
from django.contrib.contenttypes.models import ContentType


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"

    def __str__(self):
        return self.nombre


class CarpetaFamiliar(models.Model):
    """
    Asocia varios pacientes con vínculo familiares.
    """
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


class Paciente(Persona):
    """
    Datos de una persona en particular
    """
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

    carpeta_familiar = models.ForeignKey('CarpetaFamiliar', null=True, related_name='miembros', on_delete=models.SET_NULL)
    vinculo = models.CharField(max_length=50, null=True, choices=VINCULO_TYPE, help_text='Relación parental relativa a jefe de familia')
    es_jefe_familia = models.BooleanField(default=False)
    grupo_sanguineo = models.CharField(max_length=20, null=True, choices=Choices('0-', '0+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'))
    obra_social = models.ForeignKey('ObraSocial', null=True, blank=True, on_delete=models.SET_NULL)
    observaciones = models.TextField()
    datos_de_contacto = GenericRelation('core.DatoDeContacto',
                        related_query_name='pacientes',
                        null=True,
                        blank=True
                        )

    @property
    def edad(self):
        return (now().date() - self.fecha_nacimiento).days / 365

    def agregar_dato_de_contacto(self, tipo, valor):
        type_ = ContentType.objects.get_for_model(self)
        try:
            DatoDeContacto.objects.get(content_type__pk=type_.id, object_id=self.id, tipo=tipo, valor=valor)
        except DatoDeContacto.DoesNotExist:
            DatoDeContacto.objects.create(content_object=self, tipo=tipo, valor=valor)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f'{self.apellido}, {self.nombres}'


class HistoriaClinica(models.Model):
    """
    Historial de consultas que realiza un médico sobre el paciente
    """
    paciente = models.ForeignKey('Paciente', related_name='historial_clinico',
                on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Historias clinicas'

    def __str__(self):
        return '{} - {}, {}'.format(self.id, self.paciente.nombres, self.paciente.apellido)


class Consulta(models.Model):
    """
    Observaciones que realiza el médico al paciente en una consulta.
    """
    historia = models.ForeignKey('HistoriaClinica', related_name='consultas',
                    on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)
    ultima_modificacion = models.DateField(auto_now_add=True)
    diagnostico = models.TextField()
    indicaciones = models.TextField(null=True, blank=True)
    receta = models.TextField(null=True, blank=True) #podria ser un manytomany a un modelo de medicamentos
    practicas = models.TextField(null=True, blank=True)
    derivaciones = models.ManyToManyField(Profesional, blank=True)

    def __str__(self):
        return '{} - fecha: {} - paciente: {}'.format(self.id, self.fecha,
                self.historia.paciente)
