from django.conf.urls import url, include
from .views import CentroDeSaludListView


urlpatterns = [
    url(
        r'^lista.html$',
        CentroDeSaludListView.as_view(),
        name='centros-de-salud.lista'
    ),
]
