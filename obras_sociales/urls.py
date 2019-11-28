from django.conf.urls import url, include
from django.urls import path
from .views import (TableroObraSocialPorPorvinciaView, ObraSocialListView, 
                    ObraSocialCreateView, ObraSocialUpdateView)


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
        r"editar-obra-social.html/<int:pk>",
        ObraSocialUpdateView.as_view(),
        name="obras-sociales.edit",
    ),
]
