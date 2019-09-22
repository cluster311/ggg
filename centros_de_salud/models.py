from django.db import models
from address.models import AddressField


class Institucion(models.Model):
    """ Las instituciones son las administradoras finales de los centros de salud
    """
    nombre = models.CharField(max_length=290)

    def __str__(self):
        return self.nombre


class CentroDeSalud(models.Model):
    nombre = models.CharField(max_length=290)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, 
                                      null=True, blank=True,
                                      related_name='centros')
    codigo_hpgd = models.CharField(max_length=30,
                                   null=True, blank=True,
                                   help_text='Código de Hospital Público de Gestión Descentralizada. Requerido para recupero')
    
    # TODO create a PointField from GeoDjango
    """ TODO: importar datos
        info para importar del mapa / KML
        MAPA: https://www.google.com/maps/d/u/0/viewer?msa=0&mid=1vKX3YVLV4u3jLvMu22WqhYjrUzM&ll=-31.40991921483048%2C-64.17714000000001&z=11

    Calle 15 S/N (entre 18 y 19)
    Atención 7 a 17 hs 
    TE: 03543-439691 
    """
    horario_de_atencion = models.TextField(null=True, blank=True)
    direccion = AddressField(null=True, on_delete=models.SET_NULL)
    telefonos = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
