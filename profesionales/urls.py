from django.conf.urls import url, include
from django.urls import path
from .views import (
    TableroProfesionalesPorEspecialidadView,
    # revisar campos TableroProfesionalesPorLocalidadView,
    ProfesionalListView,
    ProfesionalCreateView,
    ProfesionalDetailView,
    ProfesionalUpdateView,
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
    path(
        r"detalle-profesional.html/<int:pk>",
        ProfesionalDetailView.as_view(),
        name="profesionales.detail",
    ),
    path(
        r"editar-profesional.html/<int:pk>",
        ProfesionalUpdateView.as_view(),
        name="profesionales.edit",
    ),
    # url(
    #     r"^por-departamento.html$",
    #     TableroProfesionalesPorLocalidadView.as_view(),
    #     name="profesionales.tablero.por_departamento",
    # ),
]
