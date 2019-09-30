from django.conf.urls import url, include
from .views import (TableroProfesionalesPorEspecialidadView,
                    TableroProfesionalesPorLocalidadView,
                    calendario)


urlpatterns = [
    url(r'^por-profesion.html$', TableroProfesionalesPorEspecialidadView.as_view(), name='profesionales.tablero.por_profesion'),

    url(r'^por-departamento.html$', TableroProfesionalesPorLocalidadView.as_view(), name='profesionales.tablero.por_departamento'),
    url(r'^calendario$', calendario, name='profesionales.calendario'),
    url(r'^feed$', calendario, name='profesionales.calendario'),
]