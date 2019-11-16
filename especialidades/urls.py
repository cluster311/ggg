from django.conf.urls import url, include
from django.urls import path

from .views_medidas_anexas import (MedidaAnexaListView,
                                   MedidaAnexaCreateView,
                                   MedidaAnexaDetailView,
                                   MedidaAnexaUpdateView)

from .views_medidas_anexas_en_especialidad import (MedidasAnexasEspecialidadListView,
                                                   MedidasAnexasEspecialidadCreateView,
                                                   MedidasAnexasEspecialidadDetailView,
                                                   MedidasAnexasEspecialidadUpdateView)

urlpatterns = [
    # url(
    #     r'^lista.html$',
    #     EspecialidadListView.as_view(),
    #     name='especialidades.lista'
    # ),


    url(
        r"^medidas-anexas.html$",
        MedidaAnexaListView.as_view(),
        name="especialidades.medidas_anexas",
    ),
    url(
        r"^crear-medida_anexa.html",
        MedidaAnexaCreateView.as_view(),
        name="especialidades.medidas_anexas.create",
    ),
    path(
        r"detalle-medida_anexa/<int:pk>",
        MedidaAnexaDetailView.as_view(),
        name="especialidades.medidas_anexas.detail",
    ),
    path(
        r"editar-medida_anexa/<int:pk>",
        MedidaAnexaUpdateView.as_view(),
        name="especialidades.medidas_anexas.edit",
    ),


    url(
        r"^medidas-anexas-en-especialidades.html$",
        MedidasAnexasEspecialidadListView.as_view(),
        name="especialidades.medidas-anexas-en-especialidades",
    ),
    url(
        r"^crear-medidas-anexas-en-especialidades.html",
        MedidasAnexasEspecialidadCreateView.as_view(),
        name="especialidades.medidas-anexas-en-especialidades.create",
    ),
    path(
        r"detalle-medidas-anexas-en-especialidades/<int:pk>",
        MedidasAnexasEspecialidadDetailView.as_view(),
        name="especialidades.medidas-anexas-en-especialidades.detail",
    ),
    path(
        r"editar-medidas-anexas-en-especialidades/<int:pk>",
        MedidasAnexasEspecialidadUpdateView.as_view(),
        name="especialidades.medidas-anexas-en-especialidades.edit",
    ),
]
