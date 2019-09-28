from django.db import models
from django.conf import settings
from model_utils import Choices
from address.models import AddressField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from sisa.puco import Puco
import logging
logger = logging.getLogger(__name__)


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    siglas = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    localidad = models.CharField(max_length=100, null=True, blank=True)
    domicilio = models.CharField(max_length=100, null=True, blank=True)
    cp = models.CharField(max_length=100, null=True, blank=True)
    web = models.CharField(max_length=100, null=True, blank=True)
    telefonos = models.CharField(max_length=100, null=True, blank=True)
    emails = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"

    def __str__(self):
        return f'{self.codigo} {self.nombre}'

    @classmethod
    def startdb(cls):
        osss = ObrasSocialesArgentinas()
        for rnos, oss in osss.local_json_object.items():
            print(oss)
            if oss.get('nombre', None) is None:
                continue
            defaults = {
                'nombre': oss['nombre'],
                'siglas': oss['sigla'],
                'provincia': oss['provincia'],
                'localidad': oss['localidad'],
                'domicilio': oss['domicilio'],
                'cp': oss['cp'],
                'web': oss['web'],
                # telefonos y emails
                }
            o = ObraSocial.objects.get_or_create(codigo=rnos, defaults=defaults)


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


class Persona(models.Model):
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

    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=30)
    sexo = models.CharField(max_length=20,
                    choices=Choices('masculino', 'femenino', 'otro'))
    fecha_nacimiento = models.DateField(null=True, blank=True)
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


class DatoDeContacto(models.Model):
    """Modelo generérico para guardar datos de contacto de personas o medios
    Ejemplo de uso::
        from django.contrib.contenttypes.fields import GenericRelation
        class Paciente(models.Model):
            datos_de_contacto = GenericRelation(
                'contacto.DatoDeContacto',
                related_query_name='pacientes'
            )
            ...
    """

    TIPOS = Choices(
        'teléfono', 'email', 'web', 'twitter', 'facebook',
        'instagram', 'youtube', 'skype'
    )

    tipo = models.CharField(choices=TIPOS, max_length=20)
    valor = models.CharField(max_length=100)
    # generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('tipo', 'valor', 'content_type', 'object_id'),)

    def __str__(self):
        return f'{self.tipo}: {self.valor}'
