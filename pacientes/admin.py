from django.contrib import admin
from address.models import AddressField
from address.forms import AddressWidget

from .models import (CarpetaFamiliar, Paciente, ObraSocial, Telefono,
                    HistoriaClinica, Consulta)


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

class TelefonoInLine(admin.StackedInline):
    model = Telefono
    extra = 1

class ConsultaInLine(admin.StackedInline):
    model = Consulta
    extra = 1

class HistoriaClinicaAdmin(admin.ModelAdmin):
    inlines = (ConsultaInLine, )

class PacienteAdmin(admin.ModelAdmin):
    inlines = (TelefonoInLine, )

admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)
admin.site.register(ObraSocial)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(CarpetaFamiliar, CarpetaFamiliarAdmin)
