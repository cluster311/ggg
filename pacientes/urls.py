from django.conf.urls import url, include
from django.urls import path
from .views import (
    EvolucionUpdateView,
    ConsultaListView,
    ConsultaDetailView,
    CarpetaFamiliarCreateView, PacienteCreatePopup
)


urlpatterns = [
    path(
        # debe crearse la consulta y luego llamar aquí
        r"evolucion/<int:pk>",
        EvolucionUpdateView.as_view(),
        name="pacientes.evolucion",
    ),
    
    path(
        r"<int:dni>/historia/",
        ConsultaListView.as_view(),
        name="pacientes.consulta.lista",
    ),
    path(
        r"<int:dni>/historia/<int:pk>",
        ConsultaDetailView.as_view(),
        name="pacientes.consulta.detalle",
    ),
    path(
        r"crear-carpeta-familiar/",
        CarpetaFamiliarCreateView.as_view(),
        name="pacientes.carpeta-familiar.crear",
    ),
    path(
        r"crear-carpeta-familiar/",
        CarpetaFamiliarCreateView.as_view(),
        name="pacientes.carpeta-familiar.crear",
    ),
    path(r'^paciente/create', PacienteCreatePopup, name="PacienteCreate"),

]
