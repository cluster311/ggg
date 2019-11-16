from django.conf.urls import url, include
from django.urls import path
from .views import (
    ConsultaListView,
    ConsultaDetailView,
    ConsultaCreateView,
    ConsultaUpdateView,
)


urlpatterns = [
    path(
        r"paciente/<int:dni>/historia",
        ConsultaListView.as_view(),
        name="pacientes.consulta.lista",
    ),
    path(
        r"paciente/<int:dni>/historia/<int:pk>",
        ConsultaDetailView.as_view(),
        name="pacientes.consulta.detalle",
    ),
    path(
        r"paciente/nueva-consulta",
        ConsultaCreateView.as_view(),
        name="pacientes.crear.consulta",
    ),
    path(
        r"paciente/<int:dni>/actualizar-consulta/<int:pk>",
        ConsultaUpdateView.as_view(),
        name="pacientes.actualizar.consulta",
    ),
]
