from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from .models import DatoDeContacto
from .forms import DatoDeContactoModelForm
from django.contrib.contenttypes.admin import GenericTabularInline


class ContactoAdminInline(GenericTabularInline):
    model = DatoDeContacto
    form = DatoDeContactoModelForm


class GeoAdmin(gisadmin.GeoModelAdmin):
    """
    admin para modelos con GIS
    """

    map_template = "gis/admin/fixed_openlayers.html"
    default_lon = -71.44296
    default_lat = -36.82101
    openlayers_url = (
        "https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js"
    )
    default_zoom = 4
    map_width = 1200
    map_height = 400
