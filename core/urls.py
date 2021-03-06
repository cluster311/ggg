from django.conf.urls import url
from django.urls import path
from core.views import (CIE10Autocomplete,
                        PacienteAutocomplete,
                        ProfesionalAutocomplete,
                        CentroDeSaludAutocomplete,
                        TipoPrestacionAutocomplete,
                        CarpetaFamiliarAutocomplete,
                        ServicioAutocomplete, ObraSocialAutocomplete, ObraSocialAllAutocomplete,
                        EspecialidadAutocomplete, ProfesionalFacturaAutocomplete
                        )



urlpatterns = [
    path(
        r"servicio-autocomplete/",
        ServicioAutocomplete.as_view(),
        name="servicio-autocomplete",
    ),
    path(
        r"carpeta-familiar-autocomplete/",
        CarpetaFamiliarAutocomplete.as_view(),
        name="carpeta-familiar-autocomplete",
    ),
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
        r"^obra-social-autocomplete/$",
        ObraSocialAutocomplete.as_view(),
        name="obra-social-autocomplete",
    ),
    url(
        r"^obra-social-all-autocomplete/$",
        ObraSocialAllAutocomplete.as_view(),
        name="obra-social-all-autocomplete",
    ),
    url(
        r"^profesional-autocomplete/$",
        ProfesionalAutocomplete.as_view(),
        name="profesional-autocomplete",
    ),
    url(
        r"^profesional-factura-autocomplete/$",
        ProfesionalFacturaAutocomplete.as_view(),
        name="profesional-factura-autocomplete",
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
        r"^especialidad-autocomplete/$",
        EspecialidadAutocomplete.as_view(),
        name="especialidad-autocomplete",
    ),
    url(
        r"^tipo-prestacion-autocomplete/$",
        TipoPrestacionAutocomplete.as_view(),
        name="tipo_prestacion-autocomplete",
    ),

]
