from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.conf import settings
from .models import Profesional
from calendario.models import Turno
from datetime import datetime
from pacientes.models import Consulta, Paciente
from pacientes.forms import ConsultaForm, RecetaFormset, DerivacionFormset, PrestacionFormset
from crispy_forms.utils import render_crispy_form
import logging


logger = logging.getLogger(__name__)


class ProfesionalHome(TemplateView, GroupRequiredMixin):
    """
    Home del profesional al loguearse
    """

    group_required = (settings.GRUPO_PROFESIONAL, )
    template_name = "profesionales/home_profesional.html"
    permission_required = ("pacientes.view_consulta",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = datetime.now()
        context['hoy'] = hoy
        context['estados'] = Turno.OPCIONES_ESTADO

        # sólo se muestran los turnos si está autenticado(y además debe
        # estar dentro del grupo profesionales).
        if self.request.user.is_authenticated:
            user = self.request.user
            context['user'] = user
            # que solo vea SUS turnos
            context['turnos'] = Turno.objects.filter(
                inicio__day=hoy.day,
                profesional__user=user
                ).order_by('inicio')
            if hasattr(user, 'profesional'):
                context['profesional'] = user.profesional
            else:
                # este usuario no tiene un profesional conectado
                raise PermissionDenied
        return context


class ProfesionalListView(PermissionRequiredMixin, ListView):
    model = Profesional
    permission_required = ("profesionales.view_profesional",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = Profesional.objects.filter(
                Q(nombres__icontains=q) |
                Q(apellidos__icontains=q) |
                Q(matricula_profesional__icontains=q) |
                Q(profesion__icontains=q)
                )
        else:
            objects = Profesional.objects.all()

        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        context['title'] = 'Lista de profesionales'
        context['title_url'] = 'profesionales.lista'
        context['use_search_bar'] = True
        if self.request.user.has_perm('profesionales.add_profesional'):
            context['use_add_btn'] = True
            context['add_url'] = 'profesionales.create'
        return context


class ProfesionalCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = Profesional
    permission_required = ("profesionales.view_profesional",)
    fields =  '__all__'
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales'
        context['subtitle'] = 'Nuevo Profesional'
        context['title_url'] = 'profesionales.lista'
        return context

    def get_success_url(self):
        return reverse(
            "profesionales.lista"
        )


class ProfesionalDetailView(PermissionRequiredMixin, DetailView):
    model = Profesional
    permission_required = ("profesionales.view_profesional",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales'
        context['title_url'] = 'profesionales.lista'
        return context


class ProfesionalUpdateView(PermissionRequiredMixin, UpdateView):
    model = Profesional
    permission_required = "profesionales.change_profesional"
    fields =  '__all__'
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales'
        context['subtitle'] = 'Editar Profesional'
        context['title_url'] = 'profesionales.lista'
        return context

    def get_success_url(self):
        return reverse(
            "profesionales.lista"
        )


@method_decorator(cache_page(60 * 5), name='dispatch')
class TableroProfesionalesPorEspecialidadView(
        PermissionRequiredMixin, TemplateView):
    """ mostrar datos de los profesionales """

    model = Profesional
    permission_required = ("profesionales.can_view_tablero",)
    template_name = "profesionales/tableros.html"
    # https://bootstrapious.com/tutorial/sidebar/index5.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profesionales = Profesional.objects.all()
        por_profesion = (
            profesionales.values("profesion")
            .annotate(total=Count("profesion"))
            .order_by("-total")
        )

        cols = [
            {"id": "profesion", "label": "Profesion", "type": "string"},
            {"id": "profesionales", "label": "Profesionales", "type": "number"}
            # , {'type': 'string', 'role': 'annotation'}
        ]
        rows = []
        for p in por_profesion:
            rows.append({"c": [{"v": p["profesion"]}, {"v": p["total"]}]})

        data = {"cols": cols, "rows": rows}

        chart_1 = {
            "id": "por_profesion",
            "data": data,
            "tech": "google",
            "type": "column",
            "title": "Profesionales por profesión",
            "subtitle": "",
        }
        chart_2 = {
            "id": "pie_por_profesion",
            "data": data,
            "tech": "google",
            "type": "pie",
            "title": "% Profesionales por profesión",
            "subtitle": "",
        }
        context["charts"] = [chart_1, chart_2]

        return context


class TableroProfesionalesPorLocalidadView(
        PermissionRequiredMixin, TemplateView):
    """ mostrar datos de los profesionales """

    model = Profesional
    permission_required = ("profesionales.can_view_tablero",)
    template_name = "profesionales/tableros.html"
    # https://bootstrapious.com/tutorial/sidebar/index5.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profesionales = Profesional.objects.all()
        por_profesion = (
            profesionales.values("departamento")
            .annotate(total=Count("departamento"))
            .order_by("-total")
        )

        cols = [
            {"id": "departamento", "label": "Departamento", "type": "string"},
            {"id": "profesionales", "label": "Profesionales", "type": "number"}
            # , {'type': 'string', 'role': 'annotation'}
        ]
        rows = []
        for p in por_profesion:
            rows.append({"c": [{"v": p["departamento"]}, {"v": p["total"]}]})

        data = {"cols": cols, "rows": rows}

        chart_1 = {
            "id": "por_depto",
            "data": data,
            "tech": "google",
            "type": "column",
            "title": "Profesionales por departamento",
            "subtitle": "",
        }
        chart_2 = {
            "id": "pie_por_depto",
            "data": data,
            "tech": "google",
            "type": "pie",
            "title": "% Profesionales por departamento",
            "subtitle": "",
        }
        context["charts"] = [chart_1, chart_2]

        return context
