from django.contrib import admin
from .models import (TipoDocumentoAnexo, TipoPrestacion,
                     Prestacion, DocumentoAnexo, Factura)


@admin.register(TipoDocumentoAnexo)
class Admin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(TipoPrestacion)
class TipoPrestacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'arancel', 'tipo']
    search_fields = ['nombre', 'codigo']


@admin.register(Prestacion)
class PrestacionAdmin(admin.ModelAdmin):
    def centro_de_salud(self, obj):
        return obj.consulta.centro_de_salud
    
    def profesional(self, obj):
        return obj.consulta.profesional
    
    def especialidad(self, obj):
        return obj.consulta.especialidad

    list_display = ['centro_de_salud', 'profesional', 'especialidad', 'tipo', 'cantidad', 'observaciones']


@admin.register(DocumentoAnexo)
class DocumentoAnexoAdmin(admin.ModelAdmin):
    list_display = ['prestacion', 'tipo', 'documento_adjunto']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    def centro_de_salud(self, obj):
        return obj.consulta.centro_de_salud
    
    def profesional(self, obj):
        return obj.consulta.profesional
    
    def especialidad(self, obj):
        return obj.consulta.especialidad

    list_display = ['estado', 'centro_de_salud', 'profesional', 'obra_social', 'especialidad']
    list_filter = ['consulta__centro_de_salud',
                   'obra_social',
                   'consulta__profesional',
                   'consulta__especialidad']
    
