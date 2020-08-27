from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.conf import settings

from pacientes.models import Paciente
from .forms import ObraSocialPacienteCreatePopUp
from .models import ObraSocial, ObraSocialPaciente


class ObraSocialListView(PermissionRequiredMixin, ListView):
    model = ObraSocial
    permission_required = ("obras_sociales.view_obrasocial",)
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
        if self.request.user.has_perm('obras_sociales.add_obrasocial'):
            context['use_add_btn'] = True
            context['add_url'] = 'obras-sociales.create'
        return context


class ObraSocialCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = ObraSocial
    permission_required = ("obras_sociales.add_obrasocial",)
    fields =  '__all__'
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Obras Sociales'
        context['subtitle'] = 'Nuevo obra social'
        context['title_url'] = 'obras-sociales.lista'
        return context

    def get_success_url(self):
        return reverse(
            "obras-sociales.lista"
        )


class ObraSocialUpdateView(PermissionRequiredMixin, UpdateView):
    model = ObraSocial
    permission_required = "obras_sociales.change_obrasocial"
    fields =  '__all__'
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Obras Sociales'
        context['subtitle'] = 'Editar obra social'
        context['title_url'] = 'obras-sociales.lista'
        return context

    def get_success_url(self):
        return reverse(
            "obras-sociales.lista"
        )


class ObraSocialDetailView(PermissionRequiredMixin, DetailView):
    model = ObraSocial
    permission_required = ("obras_sociales.view_obrasocial",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Obras Sociales'
        context['title_url'] = 'obras-sociales.lista'
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class TableroObraSocialPorPorvinciaView(PermissionRequiredMixin, TemplateView):
    """ mostrar datos de los profesionales """
    model = ObraSocial
    permission_required = ('obras_sociales.can_view_tablero', )
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


def ObraSocialPacienteCreatePopup(request, paciente=None):
    if request.POST:
        form = ObraSocialPacienteCreatePopUp(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(
                '<script>opener.closePopup(window, "%s", "%s", "#id_obra_social");</script>' % (instance.obra_social.pk, instance.obra_social))
    form = ObraSocialPacienteCreatePopUp(initial={'paciente': paciente})
    return render(request, "obras_sociales/obrasocial_paciente_createview.html", {"form": form})


def BuscarObraSocialPaciente(request, id_paciente, id_obra_social):
    if ObraSocialPaciente.objects.filter(paciente_id=id_paciente, obra_social_id=id_obra_social).exists():
        osp = ObraSocialPaciente.objects.get(paciente_id=id_paciente, obra_social_id=id_obra_social)
        data = {
            "encontrado": True,
            "numero_afiliado": osp.numero_afiliado
        }
    else:
        data = {"encontrado": False,
               }
    return JsonResponse(data, status=200)
