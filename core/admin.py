from django.contrib import admin
from address.models import AddressField
from address.forms import AddressWidget

from .models import CarpetaFamiliar, Paciente, ObraSocial


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

admin.site.register(Paciente)
admin.site.register(CarpetaFamiliar, CarpetaFamiliarAdmin)

@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'siglas', 'provincia', 'localidad']