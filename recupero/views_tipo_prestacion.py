from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from crispy_forms.utils import render_crispy_form

from .models import TipoPrestacion


class TipoPrestacionListView(PermissionRequiredMixin, ListView):
    """
    Lista de tipos de prestaciones habilitadas para recuperar
    """
    model = TipoPrestacion
    permission_required = ("recupero.view_tipoprestacion",)
    paginate_by = 10

    def get_queryset(self):   
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = TipoPrestacion.objects.filter(
                nombre__icontains=q)
        else:
            objects = TipoPrestacion.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'recupero.tipos-prestacion'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('recupero.add_tipoprestacion'):
            context['use_add_btn'] = True
            context['add_url'] = 'recupero.tipos-prestacion.create'
        return context


class TipoPrestacionCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = TipoPrestacion
    permission_required = ("recupero.add_tipoprestacion",)
    fields = ['nombre', 'codigo', 'descripcion', 'observaciones',
              'tipo', 'documentos_requeridos', 'documentos_sugeridos']
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'recupero.tipos-prestacion'
        return context

    def get_success_url(self):
        return reverse(
            "recupero.tipos-prestacion"
        )


class TipoPrestacionDetailView(PermissionRequiredMixin, DetailView):
    model = TipoPrestacion
    permission_required = ("recupero.view_tipoprestacion",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'recupero.tipos-prestacion'
        return context


class TipoPrestacionUpdateView(PermissionRequiredMixin, UpdateView):
    model = TipoPrestacion
    permission_required = "recupero.change_tipoprestacion"
    fields = ['nombre', 'codigo', 'descripcion', 'observaciones',
              'tipo', 'documentos_requeridos', 'documentos_sugeridos']
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'recupero.tipos-prestacion'
        return context

    def get_success_url(self):
        return reverse(
            "recupero.tipos-prestacion"
        )