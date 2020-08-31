import datetime
import json
from datetime import date

from sisa.puco import Puco
from sisa.renaper import Renaper
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from core.models import Persona, DatoDeContacto
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
from sss_beneficiarios_hospitales.data import DataBeneficiariosSSSHospital


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
    ultima_actualizacion = models.DateField(default=date.today)
    datos_de_contacto = GenericRelation(
        "core.DatoDeContacto",
        related_query_name="pacientes",
        null=True,
        blank=True
    )

    def as_json(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'numero_documento': self.numero_documento,
        }
    
    def as_anexo2_json(self):
        """ devuelve el JSON compatible con la librería Anexo2 https://github.com/cluster311/Anexo2
            Ejemplo:
                {'apellido_y_nombres': 'Juan Perez',
                    'tipo_dni': 'DNI',  # | LE | LC
                    'dni': '34100900',
                    'tipo_beneficiario': 'titular',  # | no titular | adherente
                    'parentesco': 'conyuge',  # hijo | otro
                    'sexo': 'M',  # | F
                    'edad': 88}
        """
        sexo = None
        if self.sexo == 'masculino':
            sexo = 'M'
        elif self.sexo == 'femenino':
            sexo = 'F'
        
        edad = 0 if self.edad is None else self.edad
        ret = {'apellido_y_nombres': f'{self.apellidos}, {self.nombres}',
                'tipo_dni': self.tipo_documento,
                'dni': self.numero_documento,
                'sexo': sexo,  # M | F
                'edad': edad}

        return ret

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
    def create_from_sss(cls, dni):
        logger.info(f'Buscando DNI en sss {dni}')
        dbh = DataBeneficiariosSSSHospital(user=settings.USER_SSS, password=settings.PASS_SSS)
        res = dbh.query(dni=dni)
        if res['ok']:
            tablas = res['resultados']['tablas']
            if len(tablas) == 0:
                logger.error('[SSS] Tabla no encontrada {}'.format(res['resultados']['tablas']))
                return False, f"tabla no encontrada [SSS]"
            data = tablas[0]['data']
            tam_tabla = len(tablas)
            if res['resultados']['afiliado']:
                logger.info(f'[SSS] Data Afiliado {data}')
                fecha = data['Fecha de nacimiento'].split('-')
                fecha_nac = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
                logger.info(f'SSS encontrado, buscando DNI {dni}')
                paciente, created = Paciente.objects.get_or_create(
                    numero_documento=dni,
                )
                # Solo si es creado cargo datos accesorios, de otra forma se perderían las modificaciones hechas en el sistema 
                if created:
                    logger.info('Nuevo Paciente desde SSS {}'.format(data['Apellido y nombre']))
                    apellidos = data.get('Apellido y Nombre', data.get('Apellido y nombre', None))
                    if apellidos is not None:
                        paciente.apellidos = apellidos
                    paciente.sexo = data['Sexo'].lower()
                    paciente.fecha_nacimiento = fecha_nac
                    tipo_doc = data.get('Tipo Documento', data.get('Tipo de documento', None))
                    if tipo_doc is not None:
                        paciente.tipo_documento = tipo_doc
                    paciente.save()

                oss_data = tablas[1]['data']
                oss_codigo = (''.join(filter(str.isdigit, oss_data['Código de Obra Social'])))
                logger.info('OSS desde SSS {}: {}'.format(oss_codigo, oss_data['Denominación Obra Social']))
                    
                oss, created = ObraSocial.objects.get_or_create(
                    codigo=oss_codigo,
                    defaults={
                        'nombre': oss_data['Denominación Obra Social'],
                        })
                
                # TODO chequear las OSS que tenia antes el paciente en esta fuente
                # para desactivar las que ya no existen

                # solo lo básico para saber si ya lo tengo
                logger.info('Creado OSS+paciente desde SSS {}: {}'.format(paciente, oss))
                
                osp, created = ObraSocialPaciente.objects.get_or_create(
                    data_source=settings.SOURCE_OSS_SSS,
                    paciente=paciente,
                    obra_social=oss
                )

                osp.obra_social_updated = now()
                osp.tipo_beneficiario = data['Parentesco'].lower()
                osp.save()

                if tam_tabla >= 3:
                    empleador_data = tablas[2]['data']
                    cuit_parseado = (''.join(filter(str.isdigit, oss_data['CUIT de empleador'])))
                    logger.info('Creado Empresa desde SSS {}'.format(empleador_data['Tipo Beneficiario Declarado']))
                    empresa, created = Empresa.objects.get_or_create(cuit=cuit_parseado, defaults={
                            'nombre': empleador_data['Tipo Beneficiario Declarado'],
                            })
                    fecha = empleador_data['Ultimo Período Declarado'].split('-')

                    # solo crearlo una vez e ir actualizando la fecha de último recibo
                    empp, created = EmpresaPaciente.objects.get_or_create(
                        paciente=paciente,
                        empresa=empresa
                    )
                    empp.ultimo_recibo_de_sueldo = datetime.datetime(int(fecha[1]), int(fecha[0]), 1)
                    empp.save()

                return True, paciente
            else:
                paciente, created = Paciente.objects.get_or_create(numero_documento=dni)

                # Solo si es creado cargo datos accesorios, de otra forma se perderían las modificaciones hechas en el sistema 
                if created:
                    logger.info(f'[SSS] Data Afiliado {data}')
                    # Data: : 'DU', 'Nro Documento': '20871201', 'CUIL': '27208712018'}
                    apellidos = data.get('Apellido y Nombre', data.get('Apellido y nombre', None))
                    if apellidos is not None:
                        paciente.apellidos = apellidos
                    tipo_doc = data.get('Tipo Documento', data.get('Tipo de documento', None))
                    if tipo_doc is not None:
                        paciente.tipo_documento = tipo_doc
                    paciente.save()
                    
                return True, paciente
        else:
            return False, f"Persona no encontrada [SSS]"

    @classmethod
    def create_from_sisa(cls, dni):
        logger.info(f'Busqueda desde SISA/PUCO {dni}')
                    
        rena = Renaper(dni=dni)
        # puco = Puco(dni=dni)
        resp = rena.get_info_ciudadano()
        if not resp["ok"]:
            error = f"Error de sistema SISA: {rena.last_error}"
            logger.error(error)
            return False, error

        if not resp["persona_encontrada"]:
            logger.error("Persona no encontrada en SISA")
            return False, f"Persona no encontrada: {rena.last_error}"

        logger.info(f'SISA persona encontrada: {rena.dni} {rena.nombre} {rena.apellido} RNOS: {rena.rnos}')

        paciente, created = Paciente.objects.get_or_create(numero_documento=dni)
        if created:
            paciente.tipo_documento = rena.tipo_doc
            paciente.nombres = rena.nombre
            paciente.apellidos = rena.apellido
            paciente.save()

        # Si los devuelve, setear la oss que devuelve PUCO
        if rena.rnos is not None and rena.rnos != '':
            value_default = {"nombre": rena.cobertura_social}
            logger.info(f'Crendo OSS desde SISA/PUCO {rena.rnos} {rena.cobertura_social}')
            
            oss, created = ObraSocial.objects.get_or_create(
                codigo=rena.rnos, defaults=value_default
            )

            # TODO chequear las OSS que tenia antes el paciente en esta fuente
            # para desactivar las que ya no existen
            logger.info(f'Crendo OSS+Paciente desde SISA/PUCO {paciente} {oss}')
                
            osp, created = ObraSocialPaciente.objects.get_or_create(
                data_source=settings.SOURCE_OSS_SISA,
                paciente=paciente,
                obra_social=oss,
            )
            osp.obra_social_updated = now()
            osp.save()

        return True, paciente


class Consulta(TimeStampedModel):
    """
    Reunión planificada de un paciente con un profesional
    Incluye lo que el médico hace y opina de la consulta
    """
    # en general las consultas van a venir creadas por los turnos cuando son cofirmados
    turno = models.OneToOneField('calendario.Turno',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
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
    fecha = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"{self.id} - CIE: {self.codigo_cie_principal}"
    
    def save(self, *args, **kwargs):
        """ crear la factura y analizar luego si se va a recuperar """
        super().save(*args, **kwargs)
        if not hasattr(self, 'factura'):
        # no funciona (?) if self.factura is None:
            logger.info(f'Creación Consulta {self}')
        else:
            f = self.factura
            logger.info(f'Factura {f.id} OK para la consulta {self}')


class Receta(TimeStampedModel):
    """ Cada una de las recetas que un medico le da al paciente en consulta """

    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='recetas')
    # ISSUE conectarse a algún vademecum online o crear una librería
    # https://github.com/cluster311/ggg/issues/179
    medicamento = models.CharField(max_length=290)
    posologia = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.medicamento


class Derivacion(TimeStampedModel):
    """ Cada una de las derivaciones que un medico le da al paciente en consulta """
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='derivaciones')
    especialidad = models.ForeignKey("centros_de_salud.Especialidad",on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.especialidad.nombre


class Empresa(models.Model):
    """ empresas en las que los pacientes trabajan """
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    cuit = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.nombre

class EmpresaPaciente(models.Model):
    """ Empresa donde trabaja un paciente un paciente """

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    ultimo_recibo_de_sueldo = models.DateTimeField(null=True, blank=True)
  
    def as_anexo2_json(self):
        """ devuelve el JSON compatible con la librería Anexo2 https://github.com/cluster311/Anexo2
            Ejemplo:
                {'nombre': 'Telescopios Hubble',
                   'direccion': 'Av Astronómica s/n',
                   'ultimo_recibo_de_sueldo': {'mes': 7, 'anio': 2019},
                   'cuit': '31-91203043-8'}
        """
        recibo_mes = None if self.ultimo_recibo_de_sueldo is None else self.ultimo_recibo_de_sueldo.month
        recibo_ano = None if self.ultimo_recibo_de_sueldo is None else self.ultimo_recibo_de_sueldo.year

        ret = {'nombre': self.empresa.nombre,
               'direccion': self.empresa.direccion,
               'ultimo_recibo_de_sueldo': {'mes': recibo_mes, 'anio': recibo_ano},
               'cuit': self.empresa.cuit}
        
        return ret
