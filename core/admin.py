from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from .models import DatoDeContacto
from .forms import DatoDeContactoModelForm
from django.contrib.contenttypes.admin import GenericTabularInline


class ContactoAdminInline(GenericTabularInline):
    model = DatoDeContacto
    form = DatoDeContactoModelForm


class OSMGeoAdmin(gisadmin.OSMGeoAdmin):
    """
    admin para modelos con GIS
    """

    #map_srid = 3857  # al parecer la que usa gmaps
    #map_srid = 4326  # es otra opcion usada por google
    map_template = 'gis/admin/osm.html'  # el que incluye calles y ciudades de OSM
    #map_template = 'gis/admin/openlayers.html'  # vacio, el original
    # default_lat = -31
    # default_lon = -64
    default_lon = -7144296
    default_lat = -3682101
    openlayers_url = "https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js"
    default_zoom = 12
    map_width = 1200
    map_height = 500


# admin.site.register(DatoDeContacto)