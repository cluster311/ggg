from django.contrib import admin
from .models import CentroDeSalud, Servicio, Especialidad
from core.admin import GeoAdmin


@admin.register(CentroDeSalud)
# class CentroDeSaludAdmin(gisadmin.OSMGeoAdmin):
class CentroDeSaludAdmin(GeoAdmin):

    list_display = ['nombre', 'direccion', 'horario_de_atencion', 'telefonos']
    # list_display = ['nombre', 'descripcion', 'direccion',
    #                 'horario_de_atencion', 'telefonos']
    search_fields = ['nombre', 'descripcion']


admin.site.register(Servicio)
admin.site.register(Especialidad)
