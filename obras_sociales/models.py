from django.db import models
import logging
from model_utils import Choices
from oss_ar.oss import ObrasSocialesArgentinas

logger = logging.getLogger(__name__)


class ObraSocial(models.Model):
    """ Obras sociales argentinas """
    nombre = models.CharField(max_length=240)
    codigo = models.CharField(max_length=50, unique=True)
    siglas = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    localidad = models.CharField(max_length=100, null=True, blank=True)
    domicilio = models.CharField(max_length=100, null=True, blank=True)
    cp = models.CharField(max_length=100, null=True, blank=True)
    web = models.CharField(max_length=100, null=True, blank=True)
    telefonos = models.CharField(max_length=100, null=True, blank=True)
    emails = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.codigo} {self.nombre}'

    @classmethod
    def startdb(cls):
        """ inicializar la base de datos importando desde la libreria oss_ar
            https://github.com/cluster311/obras-sociales-argentinas/"""

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
            o = ObraSocial.objects.get_or_create(
                codigo=rnos,
                defaults=defaults
            )

    class Meta:
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"
        permissions = [
            (
                "can_view_tablero",
                "Ver tableros de comandos"
            )
        ]


class ObraSocialPaciente(models.Model):
    """ cada obra social que tiene un paciente """

    paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.CASCADE,
        related_name='m2m_obras_sociales'
    )
    obra_social = models.ForeignKey(
        'ObraSocial',
        on_delete=models.CASCADE,
        related_name='pacientes'
    )
    # las llamadas al sistema SISA son limitadas y tienen costo es por esto
    # que tenemos que considerar un cache para no repetir consultas

    obra_social_updated = models.DateTimeField(null=True, blank=True)
    # los datos pueden venir de SISA, de SSSalud y quizas en el futuro desde
    # otros lugares
    data_source = models.CharField(max_length=90)
    numero_afiliado = models.CharField(max_length=50, null=True, blank=True)
    fecha_de_emision = models.DateField(null=True, blank=True)
    fecha_de_vencimiento = models.DateField(null=True, blank=True)
    tipo_beneficiario = models.CharField(
        max_length=20,
        choices=Choices("titular", "no titular", "adherente"),
        default="titular",
    )
    parentesco = models.CharField(
        max_length=20,
        choices=Choices("conyuge", "hijo", "otro"),
        default="otro",
    )

    def as_anexo2_json(self):
        """ devuelve el JSON compatible con la librería Anexo2 https://github.com/cluster311/Anexo2
            Ejemplo:
                {
                    'codigo_rnos': '800501',
                    'nombre': 'OBRA SOCIAL ACEROS PARANA',
                    'nro_carnet_obra_social': '9134818283929101',
                    'fecha_de_emision': {'dia': 11, 'mes': 9, 'anio': 2009},
                    'fecha_de_vencimiento': {'dia': 11, 'mes': 9, 'anio': 2029}
                    'tipo_beneficiario': 'no titular',
                    'parentesco': 'conyuge'
                }
        """
        emision_dia = None if self.fecha_de_emision is None else self.fecha_de_emision.day
        emision_mes = None if self.fecha_de_emision is None else self.fecha_de_emision.month
        emision_ano = None if self.fecha_de_emision is None else self.fecha_de_emision.year

        vto_dia = None if self.fecha_de_vencimiento is None else self.fecha_de_vencimiento.day
        vto_mes = None if self.fecha_de_vencimiento is None else self.fecha_de_vencimiento.month
        vto_ano = None if self.fecha_de_vencimiento is None else self.fecha_de_vencimiento.year

        ret = {
            'codigo_rnos': self.obra_social.codigo,
            'nombre': self.obra_social.nombre,
            'nro_carnet_obra_social': self.numero_afiliado,
            'fecha_de_emision': {'dia': emision_dia, 'mes': emision_mes, 'anio': emision_ano},
            'fecha_de_vencimiento': {'dia': vto_dia, 'mes': vto_mes, 'anio': vto_ano},
            'tipo_beneficiario': self.tipo_beneficiario,
            'parentesco': self.parentesco
        }

        return ret
