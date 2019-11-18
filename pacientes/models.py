from django.db import models
from core.models import Persona
from recupero.models import Factura
from profesionales.models import Profesional
from model_utils import Choices
from model_utils.models import TimeStampedModel
from address.models import AddressField
from cie10_django.models import CIE10
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from obras_sociales.models import ObraSocial, ObraSocialPaciente
import logging
logger = logging.getLogger(__name__)


class CarpetaFamiliar(models.Model):
    OPCIONES_TIPO_FAMILIA = Choices(
        ("nuclear", "Nuclear"),
        ("nuclear_ampliada", "Nuclear Ampliada"),
        ("binuclear", "Binuclear"),
        ("monoparental", "Monoparental"),
        ("extensa", "Extensa"),
        ("unipersonal", "Unipersonal"),
        ("equivalentes", "Equivalentes Familiares"),
    )
    direccion = AddressField(null=True, on_delete=models.SET_NULL)
    tipo_familia = models.CharField(
        max_length=50,
        choices=OPCIONES_TIPO_FAMILIA
    )
    apellido_principal = models.CharField(max_length=100)

    def __str__(self):
        return "Familia {0.apellido_principal} ({0.direccion})".format(self)

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
        ("Padre", "Padre"),
        ("Hijo/a", "Hijo/a"),
        ("Madre", "Madre"),
        ("Abuelo/a", "Abuelo/a"),
        ("Primo/a", "Primo/a"),
        ("Nuera/Yerno", "Nuera/Yerno"),
        ("Nieto/a", "Nieto/a"),
        ("Cuñado/a", "Cuñado/a"),
        ("Concuñado/a", "Concuñado/a"),
        ("Tio/a", "Tio/a"),
        ("Sobrino/a", "Sobrino/a"),
        ("Esposo/a", "Esposo/a"),
    )

    GRUPO_CERO_MENOS = "0-"
    GRUPO_CERO_MAS = "0+"
    GRUPO_A_MENOS = "A-"
    GRUPO_A_MAS = "A+"
    GRUPO_B_MENOS = "B-"
    GRUPO_B_MAS = "B+"
    GRUPO_AB_MENOS = "AB-"
    GRUPO_AB_MAS = "AB+"
    grupos_sanguineos = (
        (GRUPO_CERO_MENOS, "0-"),
        (GRUPO_CERO_MAS, "0+"),
        (GRUPO_A_MENOS, "A-"),
        (GRUPO_A_MAS, "A+"),
        (GRUPO_B_MENOS, "B-"),
        (GRUPO_B_MAS, "B+"),
        (GRUPO_AB_MENOS, "AB-"),
        (GRUPO_AB_MAS, "AB+"),
    )

    carpeta_familiar = models.ForeignKey(
        "CarpetaFamiliar",
        null=True,
        blank=True,
        related_name="miembros",
        on_delete=models.SET_NULL
    )
    vinculo = models.CharField(
        max_length=50,
        null=True,
        choices=VINCULO_TYPE,
        help_text="Relación parental relativa a jefe de familia",
    )
    es_jefe_familia = models.BooleanField(default=False)
    grupo_sanguineo = models.CharField(
        max_length=20, null=True, choices=grupos_sanguineos
    )
    observaciones = models.TextField(blank=True, null=True)
    datos_de_contacto = GenericRelation(
        "core.DatoDeContacto",
        related_query_name="pacientes",
        null=True,
        blank=True
    )

    @property
    def edad(self):
        return (now().date() - self.fecha_nacimiento).days / 365

    def agregar_dato_de_contacto(self, tipo, valor):
        type_ = ContentType.objects.get_for_model(self)
        try:
            DatoDeContacto.objects.get(
                content_type__pk=type_.id,
                object_id=self.id,
                tipo=tipo,
                valor=valor
            )
        except DatoDeContacto.DoesNotExist:
            DatoDeContacto.objects.create(
                content_object=self,
                tipo=tipo,
                valor=valor
            )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


    @classmethod
    def create_from_sisa(cls, dni):
        puco = Puco(dni=dni)
        resp = puco.get_info_ciudadano()
        if not resp["ok"]:
            error = f"Error de sistema: {puco.last_error}"
            logger.info(error)
            return False, error

        if not resp["persona_encontrada"]:
            logger.info("Persona no encontrada")
            return False, f"Persona no encontrada: {puco.last_error}"

        nombre_y_apellido = puco.denominacion.split(" ")
        paciente = Paciente.objects.create(
            tipo_documento=puco.tipo_doc,
            numero_documento=dni,
            nombres=nombre_y_apellido[:int(len(nombre_y_apellido)/2)],
            apellidos=nombre_y_apellido[int(len(nombre_y_apellido)/2):],
        )

        #Setear la oss que devuelve PUCO
        value_default = {"nombre": puco.cobertura_social}
        oss, created = ObraSocial.objects.get_or_create(
            codigo=puco.rnos, defaults=value_default
        )
        ObraSocialPaciente.objects.create(
            data_source=settings.SOURCE_OSS_SISA,
            paciente=paciente,
            obra_social_updated=now(),
            obra_social=oss,
        )
        return True, paciente

    def get_obras_sociales_from_sisa(self, force_update=False):
        """ Obtener la obra social de este paciente segun SISA
            Devuelve una tupla indicando
             - primero si encontro o no los datos
             - segundo el error si es que hubo uno
            """
        oss_paciente = self.m2m_obras_sociales.filter(
            data_source=settings.SOURCE_OSS_SISA
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
                return True, f"Cache valido aún {seconds_diff}"

        logger.info("Consultando PUCO")
        puco = Puco(dni=self.numero_documento)
        resp = puco.get_info_ciudadano()
        if not resp["ok"]:
            error = f"Error de sistema: {puco.last_error}"
            logger.info(error)
            return False, error

        if not resp["persona_encontrada"]:
            logger.info("Persona no encontrada")
            return False, f"Persona no encontrada: {puco.last_error}"

        logger.info("Persona encontrada")
        value_default = {"nombre": puco.cobertura_social}
        oss, created = ObraSocial.objects.get_or_create(
            codigo=puco.rnos, defaults=value_default
        )

        found = False
        for os in oss_paciente:
            if os.obra_social == oss:
                found = True
                os.obra_social_updated = now()
                os.save()
        if not found:
            # TODO: estamos detectando un cambio de OSS.
            # para tableros de control y estadísticas este dato puede
            # ser valioso de grabar
            new_oss = ObraSocialPaciente.objects.create(
                data_source=settings.SOURCE_OSS_SISA,
                paciente=self,
                obra_social_updated=now(),
                obra_social=oss,
            )

        return True, None
        # tengo aqui algunos datos que podría usar para verificar
        # puco.tipo_doc
        # nombre y apellido: puco.denominacion
        # dict con datos de la obra social: puco.oss
        """
        puco.oss = {
            'rnos': '112301',
            'exists': True,
            'nombre': (
                'OBRA SOCIAL DEL PERSONAL DE MICROS Y OMNIBUS DE MENDOZA'
            ),
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
    Reunión planificada de un paciente con un profesional
    Incluye lo que el médico hace y opina de la consulta
    """
    motivo_de_la_consulta = models.TextField(null=True, blank=True)
    paciente = models.ForeignKey(
        "Paciente",
        related_name="historial_clinico",
        on_delete=models.CASCADE,
        default="",
    )
    profesional = models.ForeignKey(
        "profesionales.Profesional",
        related_name="historial_clinico",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    centro_de_salud = models.ForeignKey(
        "centros_de_salud.CentroDeSalud",
        related_name="consultas",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    especialidad = models.ForeignKey('centros_de_salud.Especialidad',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     related_name='consultas')
    codigo_cie_principal = models.ForeignKey(CIE10, null=True, blank=True,
                                             on_delete=models.SET_NULL,
                                             related_name='diagnositicos_principales')
    codigos_cie_secundarios = models.ManyToManyField(CIE10,
                                                     blank=True,
                                                     related_name='diagnositicos_secundarios')
    evolucion = models.TextField(null=True, blank=True)
    indicaciones = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - CIE: {self.codigo_cie_principal}"
    
    def save(self, *args, **kwargs):
        """ crear la factura y analizar luego si se va a recuperar """
        super().save(*args, **kwargs)
        if not hasattr(self, 'factura'):
        # no funciona (?) if self.factura is None:
            f = Factura.objects.create(consulta=self)
            logger.info(f'Factura {f.id} creada para la consulta {self}')
        else:
            f = self.factura
            logger.info(f'Factura {f.id} OK para la consulta {self}')


class Receta(TimeStampedModel):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='recetas')
    #TODO conectarse a algún vademecum online o crear una librería
    # https://servicios.pami.org.ar/vademecum/views/consultaPublica/listado.zul
    medicamento = models.CharField(max_length=290)
    posologia = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.medicamento


class Derivacion(TimeStampedModel):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='derivaciones')
    especialidad = models.ForeignKey("centros_de_salud.Especialidad",on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.especialidad.nombre
