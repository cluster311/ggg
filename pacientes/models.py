from django.db import models
from core.models import Persona
from profesionales.models import Profesional
from model_utils import Choices
from model_utils.models import TimeStampedModel
from address.models import AddressField
from cie10_django.models import CIE10
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
import logging
logger = logging.getLogger(__name__)


class CarpetaFamiliar(models.Model):
    OPCIONES_TIPO_FAMILIA = Choices(
        ('nuclear', 'Nuclear'),
        ('nuclear_ampliada', 'Nuclear Ampliada'),
        ('binuclear', 'Binuclear'),
        ('monoparental', 'Monoparental'),
        ('extensa', 'Extensa'),
        ('unipersonal', 'Unipersonal'),
        ('equivalentes', 'Equivalentes Familiares')
    )
    direccion = AddressField(null=True, on_delete=models.SET_NULL)
    tipo_familia = models.CharField(max_length=50,
                                    choices=OPCIONES_TIPO_FAMILIA)
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

    carpeta_familiar = models.ForeignKey('CarpetaFamiliar', null=True,
                                         related_name='miembros',
                                         on_delete=models.SET_NULL)
    vinculo = models.CharField(max_length=50, null=True, choices=VINCULO_TYPE,
                               help_text=('Relación parental relativa a jefe'
                                          ' de familia'
                                          )
                               )
    es_jefe_familia = models.BooleanField(default=False)
    grupo_sanguineo = models.CharField(max_length=20, null=True,
                                       choices=Choices('0-', '0+', 'A-', 'A+',
                                                       'B-', 'B+', 'AB-',
                                                       'AB+'
                                                       )
                                       )
    observaciones = models.TextField(blank=True, null=True)
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
            DatoDeContacto.objects.get(content_type__pk=type_.id,
                                       object_id=self.id,
                                       tipo=tipo,
                                       valor=valor
                                       )
        except DatoDeContacto.DoesNotExist:
            DatoDeContacto.objects.create(content_object=self,
                                          tipo=tipo,
                                          valor=valor
                                          )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f'{self.apellidos}, {self.nombres}'

    def get_obras_sociales_from_sisa(self, force_update=False):
        """ Obtener la obra social de este paciente segun SISA
            Devuelve una tupla indicando
             - primero si encontro o no los datos
             - segundo el error si es que hubo uno
            """
        oss_paciente = self.m2m_obras_sociales.filter(data_source=settings.
                                                      SOURCE_OSS_SISA
                                                      )
        last_updated = None
        for os in oss_paciente:
            if os.obra_social_updated is not None:
                if last_updated is None:
                    last_updated = os.obra_social_updated
                elif os.obra_social_updated > last_updated:
                    last_updated = os.obra_social_updated

        if last_updated is None:
            force_update = True

        if not force_update:
            diff = now() - last_updated
            seconds_diff = diff.days * 86400 + diff.seconds
            if seconds_diff < settings.CACHED_OSS_INFO_SISA_SECONDS:
                return True, f'Cache valido aún {seconds_diff}'

        logger.info('Consultando PUCO')
        puco = Puco(dni=self.numero_documento)
        resp = puco.get_info_ciudadano()
        if not resp['ok']:
            error = f'Error de sistema: {puco.last_error}'
            logger.info(error)
            return False, error

        if not resp['persona_encontrada']:
            logger.info('Persona no encontrada')
            return False, f'Persona no encontrada: {puco.last_error}'

        logger.info('Persona encontrada')
        value_default = {'nombre': puco.cobertura_social}
        oss, created = ObraSocial.objects.get_or_create(codigo=puco.rnos,
                                                        defaults=value_default)

        found = False
        for os in oss_paciente:
            if os.obra_social == oss:
                found = True
                os.obra_social_updated = now()
                os.save()
        if not found:
            # TODO: estamos detectando un cambio de OSS.
            # para tableros de control y estadísticas este dato puede ser
            # valioso de grabar
            new_oss = ObraSocialPaciente.objects.create(
                                            data_source=settings.
                                            SOURCE_OSS_SISA,
                                            paciente=self,
                                            obra_social_updated=now(),
                                            obra_social=oss)

        return True, None
        # tengo aqui algunos datos que podría usar para verificar
        # puco.tipo_doc
        # nombre y apellido: puco.denominacion
        # dict con datos de la obra social: puco.oss
        """
        puco.oss = {
            'rnos': '112301',
            'exists': True,
            'nombre': 'OBRA SOC DEL PERSONAL DE MICROS Y OMNIBUS DE MENDOZA',
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


class Consulta(TimeStampedModel):
    """
    Observaciones que realiza el médico al paciente en una consulta.
    """
    paciente = models.ForeignKey('Paciente', related_name='historial_clinico',
                                 on_delete=models.CASCADE, default='')
    diagnostico = models.TextField()
    indicaciones = models.TextField(null=True, blank=True)
    # podria ser un manytomany a un modelo de medicamentos
    receta = models.TextField(null=True, blank=True)
    practicas = models.TextField(null=True, blank=True)
    derivaciones = models.ManyToManyField('centros_de_salud.Especialidad',
                                          blank=True)
    codigo = models.ManyToManyField(CIE10, blank=True)

    def __str__(self):
        return '{} - fecha: {} - paciente: {}, {}'.format(self.id, self.fecha,
                                                          self.paciente.
                                                          nombres,
                                                          self.paciente.
                                                          apellido)
