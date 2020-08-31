from django.conf.urls import url, include
from django.urls import path
from .views import (TableroObraSocialPorPorvinciaView, ObraSocialListView,
                    ObraSocialCreateView, ObraSocialUpdateView, ObraSocialDetailView, ObraSocialPacienteCreatePopup,
                    BuscarObraSocialPaciente)


urlpatterns = [
    url(
        r'^obra-social-por-provincia.html$',
        TableroObraSocialPorPorvinciaView.as_view(),
        name='obras-sociales.tablero.por_provincia'
    ),
    url(
        r'^lista.html$',
        ObraSocialListView.as_view(),
        name='obras-sociales.lista'
    ),
    url(
        r"^crear-obra-social.html$",
        ObraSocialCreateView.as_view(),
        name="obras-sociales.create",
    ),
    path(
        r"detalle-obra-social.html/<int:pk>",
        ObraSocialDetailView.as_view(),
        name="obras-sociales.detail",
    ),
    path(
        r"editar-obra-social.html/<int:pk>",
        ObraSocialUpdateView.as_view(),
        name="obras-sociales.edit",
    ),
    path(
        r"obrasocial-paciente/(?P<paciente>.*)$",
        ObraSocialPacienteCreatePopup,
        name="ObraSocialPacienteCreate"),
    path(
        r"buscar_obra_social_paciente/(?P<id_paciente>.*)/(?P<id_obra_social>.*)$",
        BuscarObraSocialPaciente,
        name="BuscarObraSocialPaciente"),


]
