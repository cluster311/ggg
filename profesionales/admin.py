from django.contrib import admin
from .models import Profesional

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'dni', 'matricula_profesional', 'localidad', 'departamento']
    search_fields = ['nombres', 'apellidos', 'dni', 'matricula_profesional', 'localidad', 'departamento']
    list_filter = ['localidad', 'departamento']

