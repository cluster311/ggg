from django.contrib import admin
from address.models import AddressField
from address.forms import AddressWidget
from core.admin import ContactoAdminInline
from .models import Paciente, Consulta, CarpetaFamiliar, Receta, EmpresaPaciente, Empresa, Derivacion
from recupero.models import Prestacion, TipoPrestacion
from .forms import ConsultaForm, EvolucionForm


@admin.register(CarpetaFamiliar)
class CarpetaFamiliarAdmin(admin.ModelAdmin):

    list_display = ('id', 'direccion', 'tipo_familia', 'apellido_principal')
    list_filter = ('direccion',)

    formfield_overrides = {
        AddressField: {
            "widget": AddressWidget(attrs={"style": "width: 300px;"})
        }
    }


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombres',
        'apellidos',
        'sexo',
        'fecha_nacimiento',
        'tipo_documento',
        'numero_documento',
        'nacionalidad',
    )

    inlines = [ContactoAdminInline]

class RecetaInline(admin.TabularInline):
    model = Receta
    extra = 0

class PrestacionInline(admin.TabularInline):
    '''Tabular Inline View for Prestacion'''

    model = Prestacion
    extra = 0
    autocomplete_fields = ['tipo']

class DerivacionInline(admin.TabularInline):
    '''Tabular Inline View for Derivacion'''

    model = Derivacion
    extra = 0

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'paciente',
        'turno',
        'profesional',
        'centro_de_salud',
        'obra_social',
        'especialidad',
        'codigo_cie_principal',
    )

    raw_id_fields = ('codigos_cie_secundarios',)
    autocomplete_fields = ['centro_de_salud', 'obra_social', 'codigo_cie_principal', 'codigos_cie_secundarios' ]
    inlines = [RecetaInline, PrestacionInline, DerivacionInline]


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = (
        'consulta',
        'medicamento',
        'posologia',
        'observaciones',
    )


@admin.register(Derivacion)
class DerivacionAdmin(admin.ModelAdmin):
    list_display = (
        'consulta',
        'especialidad',
        'observaciones',
    )


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'cuit')


@admin.register(EmpresaPaciente)
class EmpresaPacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'empresa', 'ultimo_recibo_de_sueldo')
    list_filter = ('paciente', 'empresa', 'ultimo_recibo_de_sueldo')
