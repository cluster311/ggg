from django.contrib import admin
from django.contrib.contenttypes import admin as contentadmin
from address.models import AddressField
from address.forms import AddressWidget
from core.admin import ContactoAdminInline
from .models import (Paciente, ObraSocial,
                    HistoriaClinica, Consulta)
from core.models import CarpetaFamiliar


class CarpetaFamiliarAdmin(admin.ModelAdmin):
    exclude = []

    formfield_overrides = {
        AddressField: {
            'widget': AddressWidget(
                attrs={
                    'style': 'width: 300px;'
                }
            )
        }
    }


class ConsultaInLine(admin.StackedInline):
    model = Consulta
    extra = 1

class HistoriaClinicaAdmin(admin.ModelAdmin):
    inlines = (ConsultaInLine, )

class PacienteAdmin(admin.ModelAdmin):
    inlines = [
        ContactoAdminInline,
    ]


admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)
admin.site.register(ObraSocial)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(CarpetaFamiliar, CarpetaFamiliarAdmin)
