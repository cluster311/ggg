from django.conf.urls import url, include
from django.urls import path
from .views import (TableroProfesionalesPorEspecialidadView,
                    TableroProfesionalesPorLocalidadView,
                    ConsultaListView,
                    ConsultaDetailView
                    )


urlpatterns = [
    url(r'^por-profesion.html$', TableroProfesionalesPorEspecialidadView.as_view(), name='profesionales.tablero.por_profesion'),
    url(r'^por-departamento.html$', TableroProfesionalesPorLocalidadView.as_view(), name='profesionales.tablero.por_departamento'),
    path(r'paciente/<int:dni>/historia', ConsultaListView.as_view(), name='profesionales.consulta.lista'),
    path(r'paciente/<int:dni>/historia/<int:pk>', ConsultaDetailView.as_view(), name='profesionales.consulta.detalle')
]