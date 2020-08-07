from django.contrib import admin
from django.contrib.contenttypes import admin as contentadmin
from address.models import AddressField
from address.forms import AddressWidget
from dal import autocomplete
from core.admin import ContactoAdminInline
from .models import Paciente, Consulta, CarpetaFamiliar, Receta, EmpresaPaciente, Empresa
from .forms import ConsultaForm


class CarpetaFamiliarAdmin(admin.ModelAdmin):
    exclude = []

    formfield_overrides = {
        AddressField: {
            "widget": AddressWidget(attrs={"style": "width: 300px;"})
        }
    }


class RecetaInline(admin.StackedInline):
    model = Receta


class ConsultaAdmin(admin.ModelAdmin):
    form = ConsultaForm
    list_display = ['id', 'paciente', 'turno', 'profesional', 'centro_de_salud', 'especialidad', 'codigo_cie_principal']
    inlines = [RecetaInline, ]


class ConsultaInLine(admin.StackedInline):
    model = Consulta
    extra = 1


class PacienteAdmin(admin.ModelAdmin):
    save_as = True
    inlines = [ContactoAdminInline]


admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(CarpetaFamiliar, CarpetaFamiliarAdmin)
admin.site.register(Empresa)
admin.site.register(EmpresaPaciente)
