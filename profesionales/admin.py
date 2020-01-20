from django.contrib import admin
from .models import Profesional
from django.conf.urls import url


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    save_as = True
    list_display = [
        "nombres",
        "apellidos",
        "numero_documento",
        "matricula_profesional"
    ]
    search_fields = [
        "nombres",
        "apellidos",
        "numero_documento",
        "matricula_profesional",
    ]
