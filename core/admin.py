from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from .models import DatoDeContacto, AppLogs
from .forms import DatoDeContactoModelForm
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(AppLogs)
class AppLogsAdmin(admin.ModelAdmin):
    list_display = ['severity', 'code', 'description', 'data']


class ContactoAdminInline(GenericTabularInline):
    model = DatoDeContacto
    form = DatoDeContactoModelForm

    extra = 1


class GeoAdmin(gisadmin.GeoModelAdmin):
    """
    admin para modelos con GIS
    """

    map_template = "gis/admin/fixed_openlayers.html"
    default_lon = -71.44296
    default_lat = -36.82101
    openlayers_url = (
        "https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/"
        "OpenLayers.js"
    )
    default_zoom = 4
    map_width = 1200
    map_height = 400
