from django.db import models
import logging
from oss_ar.oss import ObrasSocialesArgentinas


logger = logging.getLogger(__name__)


class ObraSocial(models.Model):
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
