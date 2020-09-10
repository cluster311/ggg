from django.contrib import admin
from .models import Institucion, CentroDeSalud, Especialidad, Servicio, ProfesionalesEnServicio
from core.admin import GeoAdmin

@admin.register(CentroDeSalud)
class CentroDeSaludAdmin(GeoAdmin):
    list_display = (
        'nombre',
        'institucion',
        'codigo_hpgd',
        'horario_de_atencion',
        'telefonos',
    )
    search_fields = ['nombre', 'descripcion']


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tiempo_predeterminado_turno')


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('centro', 'especialidad')
    list_filter = ('centro', 'especialidad')
    autocomplete_fields = ['centro']


@admin.register(ProfesionalesEnServicio)
class ProfesionalesEnServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'profesional', 'estado')
    list_filter = ('servicio', 'profesional')

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)