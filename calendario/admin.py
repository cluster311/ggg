from django.contrib import admin
from .models import Turno

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['estado', 'inicio', 'fin', 'servicio', 'profesional', 'paciente', 'solicitante']
    search_fields = ['paciente__apellidos', 'profesional__apellidos']
    list_filter = ['estado', 'servicio__centro', 'servicio__especialidad']
