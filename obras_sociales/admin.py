from django.contrib import admin
from .models import ObraSocial, ObraSocialPaciente


@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'codigo',
        'siglas',
        'provincia',
        'localidad',
    )
    
    list_filter = ['provincia']
    search_fields = ['nombre']


@admin.register(ObraSocialPaciente)
class ObraSocialPacienteAdmin(admin.ModelAdmin):
    list_display = (
        'paciente',
        'obra_social',
        'numero_afiliado',
        'data_source',
    )

    list_filter = ['paciente']
    search_fields = ['paciente', 'obra_social']
    autocomplete_fields = ['obra_social']