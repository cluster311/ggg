from django.conf.urls import url, include
from .views import TableroProfesionalesView


urlpatterns = [
    url(r'^por-profesion.html$', TableroProfesionalesView.as_view(), name='profesionales.tablero.por_profesion'),
    ]