from django.conf.urls import url, include
from django.urls import path
from .views import CentroDeSaludListView
from .views_servicios import (ServicioListView,
                              ServicioCreateView,
                              ServicioDetailView,
                              ServicioUpdateView)

from .views_especialidad import (EspecialidadListView,
                                 EspecialidadCreateView,
                                 EspecialidadDetailView,
                                 EspecialidadUpdateView)


urlpatterns = [
    url(
        r'^lista.html$',
        CentroDeSaludListView.as_view(),
        name='centros_de_salud.lista'
    ),


    url(
        r"^servicios.html$",
        ServicioListView.as_view(),
        name="centros_de_salud.servicios",
    ),
    url(
        r"^crear-servicio.html",
        ServicioCreateView.as_view(),
        name="centros_de_salud.servicios.create",
    ),
    path(
        r"detalle-servicio/<int:pk>",
        ServicioDetailView.as_view(),
        name="centros_de_salud.servicios.detail",
    ),
    path(
        r"editar-servicio/<int:pk>",
        ServicioUpdateView.as_view(),
        name="centros_de_salud.servicios.edit",
    ),


    url(
        r"^especialidades.html$",
        EspecialidadListView.as_view(),
        name="centros_de_salud.especialidades",
    ),
    url(
        r"^crear-especialidad.html",
        EspecialidadCreateView.as_view(),
        name="centros_de_salud.especialidades.create",
    ),
    path(
        r"detalle-especialidad/<int:pk>",
        EspecialidadDetailView.as_view(),
        name="centros_de_salud.especialidades.detail",
    ),
    path(
        r"editar-especialidad/<int:pk>",
        EspecialidadUpdateView.as_view(),
        name="centros_de_salud.especialidades.edit",
    ),
]
