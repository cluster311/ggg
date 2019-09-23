from django.contrib import admin
from .models import CentroDeSalud
from core.admin import OSMGeoAdmin


@admin.register(CentroDeSalud)
class CentroDeSaludAdmin(OSMGeoAdmin):
    list_display = ['nombre', 'direccion', 'horario_de_atencion', 'telefonos']
