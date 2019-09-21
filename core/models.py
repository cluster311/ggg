from django.db import models
from django.conf import settings
from model_utils import Choices
from address.models import AddressField
from django.utils.timezone import now
from sisa.puco import Puco
import logging
logger = logging.getLogger(__name__)


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"

    def __str__(self):
        return f'{self.codigo} {self.nombre}'
    

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
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_documento = models.CharField(max_length=20, choices=Choices('DNI', 'LC', 'LE', 'PASAPORTE', 'OTRO'))
    numero_documento = models.CharField(max_length=30, null=True, blank=True, help_text='Deje en blanco si está indocumentado')
    nacionalidad = models.CharField(max_length=50, choices=NACIONALIDAD_CHOICES)
    vinculo = models.CharField(max_length=50, null=True, choices=VINCULO_TYPE, help_text='Relación parental relativa a jefe de familia')
    es_jefe_familia = models.BooleanField(default=False)
    grupo_sanguineo = models.CharField(max_length=20, null=True, choices=Choices('0-', '0+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'))

    telefono = models.CharField(max_length=50, null=True, blank=True)
    obra_social = models.ForeignKey('ObraSocial', null=True, blank=True, on_delete=models.SET_NULL)
    # las llamadas al sistema SISA son limitadas y tienen costo
    # es por esto que tenemos que considerar un cache para no repetir consultas
    obra_social_updated = models.DateTimeField(null=True, blank=True)

    observaciones = models.TextField()


    @property
    def edad(self):
        return (now().date() - self.fecha_nacimiento).days / 365

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f'{self.apellido}, {self.nombres}'
    
    def get_obra_social(self, force_update=False):
        # obtener la obra social de este paciente segun SISA
        # devuelve una tupla indicando
        #  - primero si encontro o no los datos
        #  - segundo el error si es que hubo uno
        if self.obra_social_updated is None:
            force_update = True

        if not force_update:
            diff = now() - self.obra_social_updated
            seconds_diff = diff.days * 86400 + diff.seconds
            if seconds_diff < settings.CACHED_OSS_INFO_SISA_SECONDS:
                return True, f'Cache valido aún {seconds_diff}'

        logger.info('Consultando PUCO')
        puco = Puco(dni=self.numero_documento)
        resp = puco.get_info_ciudadano()
        if resp['ok']:
            if resp['persona_encontrada']:
                logger.info('Persona encontrada')
                oss, created = ObraSocial.objects.get_or_create(codigo=puco.rnos)
                if created:
                    logger.info(f'Nueva OSS: {puco.rnos}={puco.cobertura_social}')
                    oss.nombre = puco.cobertura_social
                    oss.save()

                if self.obra_social != oss:
                    # TODO: estamos detectando un cambio de OSS.
                    # para tableros de control y estadísticas este dato puede ser valioso de grabar
                    pass
                    
                self.obra_social = oss
                self.obra_social_updated = now()
                return True, None
                # tengo aqui algunos datos que podría usar para verificar
                # puco.tipo_doc
                # nombre y apellido: puco.denominacion
                # dict con datos de la obra social: puco.oss
                """
                puco.oss = {
                    'rnos': '112301',
                    'exists': True,
                    'nombre': 'OBRA SOCIAL DEL PERSONAL DE MICROS Y OMNIBUS DE MENDOZA',
                    'tipo_de_cobertura': 'Obra social',
                    'sigla': 'OSPEMOM',
                    'provincia': 'Mendoza',
                    'localidad': 'MENDOZA',
                    'domicilio': 'CATAMARCA 382',
                    'cp': '5500',
                    'telefonos': ['0261-4-203283', '0261-4-203342'],
                    'emails': ['ospemom@ospemom.org.ar'],
                    'web': None,
                    'sources': ['SISA', 'SSSalud']
                    }
                """

            else:
                logger.info('Persona no encontrada')
                return False, f'Persona no encontrada: {puco.last_error}'
        else:
            error = f'Error de sistema: {puco.last_error}'
            logger.info(error)
            return False, error
    