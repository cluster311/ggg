from django.contrib import admin
from django.contrib.contenttypes import admin as contentadmin
from address.models import AddressField
from address.forms import AddressWidget
from dal import autocomplete
from core.admin import ContactoAdminInline
from .models import Paciente, Consulta, CarpetaFamiliar
from .forms import ConsultaForm


class CarpetaFamiliarAdmin(admin.ModelAdmin):
    exclude = []

    formfield_overrides = {
        AddressField: {
            "widget": AddressWidget(attrs={"style": "width: 300px;"})
        }
    }


class ConsultaAdmin(admin.ModelAdmin):
    form = ConsultaForm


class ConsultaInLine(admin.StackedInline):
    model = Consulta
    extra = 1


class PacienteAdmin(admin.ModelAdmin):
    inlines = [ContactoAdminInline]


admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(CarpetaFamiliar, CarpetaFamiliarAdmin)
