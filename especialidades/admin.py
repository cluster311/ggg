from django.contrib import admin
from .models import MedidaAnexaEnConsulta, MedidaAnexa, MedidasAnexasEspecialidad


@admin.register(MedidaAnexa)
class MedidaAnexaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'observaciones_para_el_que_mide']


@admin.register(MedidasAnexasEspecialidad)
class MedidasAnexasEspecialidadAdmin(admin.ModelAdmin):
    list_display = (
        'especialidad',
        'medida',
        'obligatorio',
        'observaciones_para_el_que_mide',
    )

@admin.register(MedidaAnexaEnConsulta)
class MedidaAnexaEnConsultaAdmin(admin.ModelAdmin):
    list_display = ['consulta', 'medida', 'valor']