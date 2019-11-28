from django.conf.urls import url, include
from .views import TableroObraSocialPorPorvinciaView, ObraSocialListView, ObraSocialCreateView


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
]
