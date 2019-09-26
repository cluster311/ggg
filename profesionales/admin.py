from django.contrib import admin
from .models import Profesional

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'dni', 'matricula_profesional']
    search_fields = ['nombres', 'apellidos', 'dni', 'matricula_profesional']
