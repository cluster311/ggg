from django.conf.urls import url
from core.views import CIE10Autocomplete, PacienteAutocomplete


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
]
