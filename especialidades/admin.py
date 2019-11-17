from django.contrib import admin
from .models import MedidaAnexaEnConsulta


@admin.register(MedidaAnexaEnConsulta)
class MedidaAnexaEnConsultaAdmin(admin.ModelAdmin):
    list_display = ['consulta', 'medida', 'valor']
