from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from crispy_forms.utils import render_crispy_form

from .models import Especialidad


class EspecialidadListView(PermissionRequiredMixin, ListView):
    """
    Lista de Especialidades
    """
    model = Especialidad
    permission_required = ("view_especialidad",)
    paginate_by = 10

    def get_queryset(self):   
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = Especialidad.objects.filter(
                nombre__icontains=q)
        else:
            objects = Especialidad.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Especialidades'
        context['title_url'] = 'centros_de_salud.especialidades'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('centros_de_salud.add_especialidad'):
            context['use_add_btn'] = True
            context['add_url'] = 'centros_de_salud.especialidades.create'
        return context


class EspecialidadCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = Especialidad
    permission_required = ("view_especialidad",)
    fields = ['nombre']
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Especialidades'
        context['title_url'] = 'centros_de_salud.especialidades'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.especialidades"
        )


class EspecialidadDetailView(PermissionRequiredMixin, DetailView):
    model = Especialidad
    permission_required = ("view_especialidad",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Especialidades'
        context['title_url'] = 'centros_de_salud.especialidades'
        return context


class EspecialidadUpdateView(PermissionRequiredMixin, UpdateView):
    model = Especialidad
    permission_required = "change_especialidad"
    fields = ['nombre']
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Especialidades'
        context['title_url'] = 'centros_de_salud.especialidades'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.especialidades"
        )