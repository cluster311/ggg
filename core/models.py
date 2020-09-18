from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from model_utils import Choices
from address.models import AddressField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)
private_file_storage = FileSystemStorage(location=settings.PRIVATE_FILES_ROOT)

class Persona(models.Model):
    VINCULO_TYPE = Choices(
        ('Padre', 'Padre'),
        ('Hijo/a', 'Hijo/a'),
        ('Madre', 'Madre'),
        ('Abuelo/a', 'Abuelo/a'),
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
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=30)
    sexo = models.CharField(
        max_length=20,
        choices=Choices("masculino", "femenino", "otro"),
        default="masculino",
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_documento = models.CharField(
        max_length=40,
        default="DNI",
        choices=Choices("DNI", "LC", "LE", "PASAPORTE", "OTRO"),
    )
    numero_documento = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="Deje en blanco si está indocumentado",
    )
    nacionalidad = models.CharField(
        max_length=50,
        choices=NACIONALIDAD_CHOICES,
        default=NACIONALIDAD_CHOICES.argentina
    )

    @property
    def edad(self):
        if self.fecha_nacimiento is None:
            return None
        return int((now().date() - self.fecha_nacimiento).days / 365.2425)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}, {}".format(self.apellido, self.nombres)


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
        "teléfono",
        "email",
        "web",
        "twitter",
        "facebook",
        "instagram",
        "youtube",
        "skype",
    )

    tipo = models.CharField(choices=TIPOS, max_length=20)
    valor = models.CharField(max_length=100)
    # generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = (("tipo", "valor", "content_type", "object_id"),)

    def __str__(self):
        return f"{self.tipo}: {self.valor}"


class AppLogs(models.Model):
    """ logs varios de cosas relevantes del sistema """
    severity = models.PositiveSmallIntegerField(default=0)
    code = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.code
