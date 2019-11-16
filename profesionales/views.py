from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.conf import settings
from .models import Profesional
from pacientes.models import Consulta
from pacientes.forms import ConsultaForm, RecetaFormset, DerivacionFormset, PrestacionFormset
from crispy_forms.utils import render_crispy_form
import logging
logger = logging.getLogger(__name__)


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProfesionalListView(PermissionRequiredMixin, ListView):
    model = Profesional
    permission_required = ("view_profesional",)
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
    permission_required = ("view_profesional",)
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
    permission_required = ("view_profesional",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales'
        context['title_url'] = 'profesionales.lista'
        return context


class ProfesionalUpdateView(PermissionRequiredMixin, UpdateView):
    model = Profesional
    permission_required = "change_profesional"
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
    permission_required = ("can_view_tablero",)
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
    permission_required = ("can_view_tablero",)
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


class ConsultaListView(PermissionRequiredMixin, ListView):
    """
    Lista de consultas de un paciente para la interfaz del profesional.
    """

    model = Consulta
    permission_required = ("can_view_tablero",)
    template_name = "profesionales/consulta_listview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dni = self.kwargs["dni"]
        consultas = Consulta.objects.filter(paciente__numero_documento=dni)
        context["consultas"] = consultas

        return context


class ConsultaDetailView(PermissionRequiredMixin, DetailView):
    """
    Detalle de un objeto Consulta
    """

    model = Consulta
    permission_required = ("can_view_tablero",)
    template_name = "profesionales/consulta_detailview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = self.object.created.strftime("%d/%m/%Y")

        return context


class ConsultaMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = getattr(self, 'object', None)
        
        data = self.request.POST if self.request.method == "POST" else None
        
        context["recetas_frm"] = RecetaFormset(data, prefix='Recetas', instance=instance)
        context["derivaciones_frm"] = DerivacionFormset(data, prefix='Derivaciones', instance=instance)
        context["prestaciones_frm"] = PrestacionFormset(data, prefix='Prestaciones', instance=instance)
       
        context["formsets"] = [
            context["recetas_frm"],
            context["derivaciones_frm"],
            context["prestaciones_frm"]
        ]        
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        
        rs = context["recetas_frm"]
        ds = context["derivaciones_frm"]
        ps = context["prestaciones_frm"]

        self.object = form.save()
        
        if rs.is_valid():
            rs.instance = self.object
            rs.save()
        
        if ds.is_valid():
            ds.instance = self.object
            ds.save()
        
        if ps.is_valid():
            ps.instance = self.object
            ps.save()
        
        return super().form_valid(form)


class ConsultaCreateView(ConsultaMixin, SuccessMessageMixin, PermissionRequiredMixin,
                         CreateView, ):
    """Crea un objeto Consulta."""

    permission_required = ("can_view_tablero",)
    template_name = "profesionales/consulta_createview.html"
    form_class = ConsultaForm
    success_message = "Datos guardados con éxito."

    def get_success_url(self):
        return reverse(
            "profesionales.consulta.lista",
            kwargs=({"dni": self.object.paciente.numero_documento}),
        )


class ConsultaUpdateView(ConsultaMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """
    Actualiza un objeto Consulta
    """

    model = Consulta
    form_class = ConsultaForm
    permission_required = ("can_view_tablero",)
    
    template_name = "profesionales/consulta_updateview.html"
    success_message = "Datos actualizados con éxito."

    
    def get_object(self):
        return get_object_or_404(Consulta, 
            paciente__numero_documento=self.kwargs.get('dni'),
            pk=self.kwargs.get('pk')
        ) 

    def get_success_url(self):
        return reverse(
            "profesionales.consulta.lista",
            kwargs=({"dni": self.object.paciente.numero_documento}),
        )
