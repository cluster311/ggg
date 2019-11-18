from django.contrib import admin
from .models import ObraSocial, ObraSocialPaciente


@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'siglas']


@admin.register(ObraSocialPaciente)
class ObraSocialPacienteAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'obra_social', 'data_source']

