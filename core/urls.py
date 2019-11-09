from django.conf.urls import url
from django.urls import path
from core.views import (CIE10Autocomplete,
                        PacienteAutocomplete,
                        ProfesionalAutocomplete,
                        CentroDeSaludAutocomplete,
                        TipoPrestacionAutocomplete
                        )


urlpatterns = [
    url(
        r"^cie10-autocomplete/$",
        CIE10Autocomplete.as_view(),
        name="cie10-autocomplete"
    ),
    url(
        r"^paciente-autocomplete/$",
        PacienteAutocomplete.as_view(),
        name="paciente-autocomplete",
    ),
    url(
        r"^profesional-autocomplete/$",
        ProfesionalAutocomplete.as_view(),
        name="profesional-autocomplete",
    ),
    path(
        r"profesional-autocomplete-por-servicio/<int:servicio_id>",
        ProfesionalAutocomplete.as_view(),
        name="profesional-autocomplete-por-servicio",
    ),
    url(
        r"^centro-de-salud-autocomplete/$",
        CentroDeSaludAutocomplete.as_view(),
        name="centro_de_salud-autocomplete",
    ),
    url(
        r"^tipo-prestacion-autocomplete/$",
        TipoPrestacionAutocomplete.as_view(),
        name="tipo_prestacion-autocomplete",
    ),
    
]
