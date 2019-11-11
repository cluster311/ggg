from django.conf.urls import url, include
from django.urls import path
from .views_usuarios_en_centros import (UsuarioEnCentroDeSaludListView,
                                        UsuarioEnCentroDeSaludCreateView,
                                        UsuarioEnCentroDeSaludDetailView,
                                        UsuarioEnCentroDeSaludUpdateView)
from .views import elegir_centro

urlpatterns = [

    url(
        r"^centro-de-salud.html$",
        UsuarioEnCentroDeSaludListView.as_view(),
        name="usuarios.en-centro-de-salud",
    ),
    url(
        r"^crear-en-centro-de-salud.html",
        UsuarioEnCentroDeSaludCreateView.as_view(),
        name="usuarios.en-centro-de-salud.create",
    ),
    path(
        r"detalle-en-centro-de-salud/<int:pk>",
        UsuarioEnCentroDeSaludDetailView.as_view(),
        name="usuarios.en-centro-de-salud.detail",
    ),
    path(
        r"editar-en-centro-de-salud/<int:pk>",
        UsuarioEnCentroDeSaludUpdateView.as_view(),
        name="usuarios.en-centro-de-salud.edit",
    ),

    url(r'^elegir_centro/$', elegir_centro, name='usuarios.elegir-centro'),


]
