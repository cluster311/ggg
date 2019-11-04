from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import ObraSocial


@method_decorator(cache_page(60 * 5), name='dispatch')
class ObraSocialListView(PermissionRequiredMixin, ListView):
    model = ObraSocial
    permission_required = ("view_obrasocial",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = ObraSocial.objects.filter(
                Q(nombre__icontains=q) |
                Q(codigo__icontains=q) |
                Q(siglas__icontains=q)
                )
        else:
            objects = ObraSocial.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        context['title'] = 'Lista de Obras sociales'
        context['title_url'] = 'obras-sociales.lista'
        context['use_search_bar'] = True
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class TableroObraSocialPorPorvinciaView(PermissionRequiredMixin, TemplateView):
    """ mostrar datos de los profesionales """
    model = ObraSocial
    permission_required = ('can_view_tablero', )
    template_name = 'profesionales/tableros.html'
    # https://bootstrapious.com/tutorial/sidebar/index5.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oss = ObraSocial.objects.all()
        por_provincia = oss.values('provincia').annotate(
            total=Count('provincia')
        ).order_by('-total')

        cols = [
            {'id': 'provincia', 'label': 'Provincia', 'type': 'string'},
            {'id': 'total', 'label': 'total', 'type': 'number'}
            ]
        rows = []
        for p in por_provincia:
            provincia = 'S/D' if p['provincia'] is None else p['provincia']
            rows.append(
                {'c': [
                    {'v': provincia},
                    {'v': p['total']}
                    ]}
            )

        data = {'cols': cols, 'rows': rows}

        chart_1 = {'id': 'por_provincia',
                   'data': data,
                   'tech': 'google',
                   'type': 'column',
                   'title': 'Obras Sociales por provincia',
                   'subtitle': '',
                   }
        chart_2 = {'id': 'pie_por_provincia',
                   'data': data,
                   'tech': 'google',
                   'type': 'pie',
                   'title': '% Obras sociales por provincia',
                   'subtitle': '',
                   }
        context['charts'] = [
                chart_1,
                chart_2
            ]

        return context
