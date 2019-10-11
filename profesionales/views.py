from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.conf import settings
from .models import Profesional
from pacientes.models import Consulta
from pacientes.forms import ConsultaForm


def index (request):
    """
    Interfaz principal para un profesional
    """
    return render_to_response('index.html')


@method_decorator(cache_page(60 * 5), name='dispatch')
class TableroProfesionalesPorEspecialidadView(PermissionRequiredMixin, TemplateView):
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
    

class TableroProfesionalesPorLocalidadView(PermissionRequiredMixin, TemplateView):
    """ mostrar datos de los profesionales """
    model = Profesional
    permission_required = ('can_view_tablero', )
    template_name = 'profesionales/tableros.html'
    # https://bootstrapious.com/tutorial/sidebar/index5.html
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profesionales = Profesional.objects.all()
        por_profesion = profesionales.values('departamento').annotate(total=Count('departamento')).order_by('-total')

        cols = [
            {'id': 'departamento', 'label': 'Departamento', 'type': 'string'},
            {'id': 'profesionales', 'label': 'Profesionales', 'type': 'number'}
            # , {'type': 'string', 'role': 'annotation'}
            ]
        rows = []
        for p in por_profesion:
            rows.append(
                {'c': [
                    {'v': p['departamento']},
                    {'v': p['total']}
                    ]}
            )

        data = {'cols': cols, 'rows': rows}

        chart_1 = {'id': 'por_depto',
                   'data': data,
                   'tech': 'google',
                   'type': 'column',
                   'title': 'Profesionales por departamento',
                   'subtitle': '',
                   }
        chart_2 = {'id': 'pie_por_depto',
                   'data': data,
                   'tech': 'google',
                   'type': 'pie',
                   'title': '% Profesionales por departamento',
                   'subtitle': '',
                   }
        context['charts'] = [
                chart_1,
                chart_2
            ]
        
        return context


class ConsultaListView(PermissionRequiredMixin, ListView):
    """
    Lista de consultas de un paciente para la interfaz del profesional.
    """
    model = Consulta
    permission_required = ('can_view_tablero', )
    template_name = 'profesionales/consulta_listview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dni = self.kwargs['dni']
        consultas = Consulta.objects.filter(paciente__numero_documento=dni)
        context['consultas'] = consultas

        return context


class ConsultaDetailView(PermissionRequiredMixin, DetailView):
    """
    Detalle de un objeto Consulta
    """
    model = Consulta
    permission_required = ('can_view_tablero', )
    template_name = 'profesionales/consulta_detailview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fecha'] = self.object.modified.strftime('%d/%m/%Y')
        return context


class ConsultaCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    """
    Crea un objeto Consulta
    """
    # model = Consulta
    permission_required = ('can_view_tablero', )
    template_name = 'profesionales/consulta_createview.html'
    form_class = ConsultaForm
    success_message = "Datos guardados con éxito."

    def get_success_url(self):
        # messages.success(self.request, 'Consulta guardada con éxito.')
        return reverse('profesionales.consulta.lista',
                        kwargs=({'dni': self.object.paciente.numero_documento}))
