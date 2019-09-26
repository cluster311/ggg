from django.views.generic import TemplateView
from django.db.models import Count
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Profesional


@method_decorator(cache_page(60 * 5), name='dispatch')
class TableroProfesionalesView(PermissionRequiredMixin, TemplateView):
    """ mostrar datos de los profesionales """
    model = Profesional
    permission_required = ('can_view_tablero', )
    template_name = 'profesionales/tableros.html'
    # https://bootstrapious.com/tutorial/sidebar/index5.html
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profesionales = Profesional.objects.all()
        por_profesion = profesionales.values('profesion').annotate(total=Count('profesion')).order_by('-total')

        cols = [
            {'id': 'profesion', 'label': 'Profesion', 'type': 'string'},
            {'id': 'profesionales', 'label': 'Profesionales', 'type': 'number'}
            # , {'type': 'string', 'role': 'annotation'}
            ]
        rows = []
        for p in por_profesion:
            rows.append(
                {'c': [
                    {'v': p['profesion']},
                    {'v': p['total']}
                    ]}
            )

        data = {'cols': cols, 'rows': rows}

        chart_1 = {'id': 'por_profesion',
                   'data': data,
                   'tech': 'google',
                   'type': 'column',
                   'title': 'Profesionales por profesión',
                   'subtitle': '',
                   }
        chart_2 = {'id': 'pie_por_profesion',
                   'data': data,
                   'tech': 'google',
                   'type': 'pie',
                   'title': '% Profesionales por profesión',
                   'subtitle': '',
                   }
        context['charts'] = [
                chart_1,
                chart_2
            ]
        
        return context
