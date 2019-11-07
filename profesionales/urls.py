from django.conf.urls import url, include
from django.urls import path
from .views import (
    TableroProfesionalesPorEspecialidadView,
    TableroProfesionalesPorLocalidadView,
    ConsultaListView,
    ConsultaDetailView,
    ConsultaCreateView,
    ConsultaUpdateView,
    ProfesionalListView,
    ProfesionalCreateView,
)


urlpatterns = [
    url(
        r"^por-profesion.html$",
        TableroProfesionalesPorEspecialidadView.as_view(),
        name="profesionales.tablero.por_profesion",
    ),
    url(
        r"^lista.html$",
        ProfesionalListView.as_view(),
        name="profesionales.lista",
    ),
    url(
        r"^crear-profesional.html$",
        ProfesionalCreateView.as_view(),
        name="profesionales.create",
    ),
    url(
        r"^por-departamento.html$",
        TableroProfesionalesPorLocalidadView.as_view(),
        name="profesionales.tablero.por_departamento",
    ),
    path(
        r"paciente/<int:dni>/historia",
        ConsultaListView.as_view(),
        name="profesionales.consulta.lista",
    ),
    path(
        r"paciente/<int:dni>/historia/<int:pk>",
        ConsultaDetailView.as_view(),
        name="profesionales.consulta.detalle",
    ),
    path(
        r"paciente/nueva-consulta",
        ConsultaCreateView.as_view(),
        name="profesionales.crear.consulta",
    ),
    path(
        r"paciente/<int:dni>/actualizar-consulta/<int:pk>",
        ConsultaUpdateView.as_view(),
        name="profesionales.actualizar.consulta",
    ),
]
