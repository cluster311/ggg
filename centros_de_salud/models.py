from django.db import models
from address.models import AddressField


class CentroDeSalud(models.Model):
    nombre = models.CharField(max_length=290)
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
