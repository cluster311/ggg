from django.conf.urls import url, include
from .views import TableroObraSocialPorPorvinciaView


urlpatterns = [
    url(r'^obra-social-por-provincia.html$', TableroObraSocialPorPorvinciaView.as_view(), name='obras-sociales.tablero.por_provincia'),
    ]