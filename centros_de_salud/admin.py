from django.contrib import admin
from .models import CentroDeSalud
from django.contrib.gis import admin as gisadmin


@admin.register(CentroDeSalud)
# class CentroDeSaludAdmin(gisadmin.OSMGeoAdmin):
class CentroDeSaludAdmin(gisadmin.GeoModelAdmin):

    map_template = 'gis/admin/fixed_openlayers.html'
    default_lon = -71.44296
    default_lat = -36.82101
    default_zoom = 4
    map_width = 1200
    map_height = 400

    list_display = ['nombre', 'ubicacion', 'descripcion', 'direccion',
                    'horario_de_atencion', 'telefonos']
