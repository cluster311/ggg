from django.conf.urls import url, include
from django.urls import path
from .views import (CentroDeSaludListView, CentroDeSaludCreateView,
                    CentroDeSaludDetailView, CentroDeSaludUpdateView)
from .views_servicios import (ServicioListView,
                              ServicioCreateView,
                              ServicioDetailView,
                              ServicioUpdateView,
                              servicios_by_especialidad)

from .views_especialidad import (EspecialidadListView,
                                 EspecialidadCreateView,
                                 EspecialidadDetailView,
                                 EspecialidadUpdateView)

from .views_profesionales_en_servicios import (ProfesionalesEnServicioListView,
                                               ProfesionalesEnServicioCreateView,
                                               ProfesionalesEnServicioDetailView,
                                               ProfesionalesEnServicioUpdateView)

urlpatterns = [
    url(
        r'^lista.html$',
        CentroDeSaludListView.as_view(),
        name='centros_de_salud.lista'
    ),
    url(
        r"^crear.html$",
        CentroDeSaludCreateView.as_view(),
        name="centros_de_salud.create",
    ),
    path(
        r"detalle.html/<int:pk>",
        CentroDeSaludDetailView.as_view(),
        name="centros_de_salud.detail",
    ),
    path(
        r"editar.html/<int:pk>",
        CentroDeSaludUpdateView.as_view(),
        name="centros_de_salud.edit",
    ),
    url(
        r"^servicios.html$",
        ServicioListView.as_view(),
        name="centros_de_salud.servicios",
    ),
    url(
        r"^crear-servicio.html$",
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
        r"^crear-especialidad.html$",
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


    url(
        r"^profesionales-en-servicio.html$",
        ProfesionalesEnServicioListView.as_view(),
        name="centros_de_salud.profesionales-en-servicio",
    ),
    url(
        r"^crear-profesional-en-servicio.html$",
        ProfesionalesEnServicioCreateView.as_view(),
        name="centros_de_salud.profesionales-en-servicio.create",
    ),
    path(
        r"detalle-profesional-en-servicio/<int:pk>",
        ProfesionalesEnServicioDetailView.as_view(),
        name="centros_de_salud.profesionales-en-servicio.detail",
    ),
    path(
        r"editar-profesional-en-servicio/<int:pk>",
        ProfesionalesEnServicioUpdateView.as_view(),
        name="centros_de_salud.profesionales-en-servicio.edit",
    ),

    path(
        r"servicio-by-especialidad/<int:pk>",
        servicios_by_especialidad,
        name="centros_de_salud.servicio-by-especialidad",
    ),
]
