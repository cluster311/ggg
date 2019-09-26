from django.contrib.gis.db import models
from address.models import AddressField
from tinymce.models import HTMLField


class CentroDeSalud(models.Model):
    nombre = models.CharField(max_length=290)
    descripcion = HTMLField(null=True, blank=True)
    horario_de_atencion = models.TextField(null=True, blank=True)
    direccion = AddressField(null=True, on_delete=models.SET_NULL)
    telefonos = models.TextField(null=True, blank=True)

    ubicacion = models.PointField(null=True, blank=True)

    def __str__(self):
        return self.nombre     
