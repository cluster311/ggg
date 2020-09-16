from django.contrib import admin

from .models import TipoDocumentoAnexo, TipoPrestacion, Prestacion, DocumentoAnexo, Factura, FacturaPrestacion


@admin.register(TipoDocumentoAnexo)
class TipoDocumentoAnexoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ['nombre']


@admin.register(TipoPrestacion)
class TipoPrestacionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'codigo',
        'arancel',
        'tipo',
    )
    search_fields = ['nombre', 'codigo']


@admin.register(Prestacion)
class PrestacionAdmin(admin.ModelAdmin):
    def centro_de_salud(self, obj):
        return obj.consulta.centro_de_salud
    
    def profesional(self, obj):
        return obj.consulta.profesional
    
    def especialidad(self, obj):
        return obj.consulta.especialidad

    list_display = (
        'consulta',
        'centro_de_salud',
        'profesional',
        'especialidad',
        'tipo',
        'cantidad',
        'observaciones',
    )
    search_fields = ['tipo']
    autocomplete_fields = ['tipo']


@admin.register(DocumentoAnexo)
class DocumentoAnexoAdmin(admin.ModelAdmin):
    list_display = (
        'prestacion',
        'tipo',
        'documento_adjunto',
    )

class FacturaPrestacionInline(admin.TabularInline):
    model = FacturaPrestacion

    fields = ['tipo', 'cantidad','observaciones']
    extra = 0
    autocomplete_fields = ['tipo']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'estado',
        'consulta',
        'obra_social',
        'fecha_atencion',
        'centro_de_salud',
        'paciente',
        'codigo_cie_principal',
        'profesional',
        'especialidad',
    )
    list_filter = (
        'paciente',
        'profesional',
        'especialidad',
    )
    raw_id_fields = ('codigos_cie_secundarios',)
    autocomplete_fields = ['obra_social', 'centro_de_salud', 'codigo_cie_principal', 'codigos_cie_secundarios']

    inlines = [FacturaPrestacionInline, ]


@admin.register(FacturaPrestacion)
class FacturaPrestacionAdmin(admin.ModelAdmin):
    list_display = (
        'factura',
        'tipo',
        'cantidad',
        'observaciones',
    )

    autocomplete_fields = ['tipo']
