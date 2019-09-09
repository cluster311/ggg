from django.contrib import admin
from .models import CentroDeSalud

@admin.register(CentroDeSalud)
class CentroDeSaludAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'horario_de_atencion', 'telefonos']
