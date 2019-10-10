from django.conf.urls import url, include
from django.urls import path
from .views import (index,
                    TableroProfesionalesPorEspecialidadView,
                    TableroProfesionalesPorLocalidadView,
                    ConsultaListView,
                    ConsultaDetailView,
                    ConsultaCreateView
                    )


urlpatterns = [
    path(r'main',
         index,
         name='profesionales.index'
        ),
    url(r'^por-profesion.html$',
        TableroProfesionalesPorEspecialidadView.as_view(),
        name='profesionales.tablero.por_profesion'
        ),
    url(r'^por-departamento.html$',
        TableroProfesionalesPorLocalidadView.as_view(),
        name='profesionales.tablero.por_departamento'
        ),
    path(r'paciente/<int:dni>/historia',
         ConsultaListView.as_view(),
         name='profesionales.consulta.lista'
        ),
    path(r'paciente/<int:dni>/historia/<int:pk>',
         ConsultaDetailView.as_view(),
         name='profesionales.consulta.detalle'
        ),
    path(r'paciente/nueva-consulta',
         ConsultaCreateView.as_view(),
         name='profesionales.crear.consulta'
        )
]