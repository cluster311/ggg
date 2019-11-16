from django.conf.urls import url, include
from django.urls import path
from .views import (
    EvolucionCreateView,
    ConsultaListView,
    ConsultaDetailView,
    ConsultaCreateView,
    ConsultaUpdateView,
)


urlpatterns = [
    path(
        r"evolucion",
        EvolucionCreateView.as_view(),
        name="pacientes.evolucion",
    ),
    
    path(
        r"<int:dni>/historia",
        ConsultaListView.as_view(),
        name="pacientes.consulta.lista",
    ),
    path(
        r"<int:dni>/historia/<int:pk>",
        ConsultaDetailView.as_view(),
        name="pacientes.consulta.detalle",
    ),
    path(
        r"nueva-consulta",
        ConsultaCreateView.as_view(),
        name="pacientes.crear.consulta",
    ),
    path(
        r"<int:dni>/actualizar-consulta/<int:pk>",
        ConsultaUpdateView.as_view(),
        name="pacientes.actualizar.consulta",
    ),
]
