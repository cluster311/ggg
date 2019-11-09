from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from crispy_forms.utils import render_crispy_form

from .models import Servicio


class ServicioListView(PermissionRequiredMixin, ListView):
    """
    Lista de tipos de prestaciones habilitadas para recuperar
    """
    model = Servicio
    permission_required = ("view_servicio",)
    paginate_by = 10

    def get_queryset(self):   
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = Servicio.objects.filter(
                nombre__icontains=q)
        else:
            objects = Servicio.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'centros_de_salud.servicios'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('centros_de_salud.add_servicio'):
            context['use_add_btn'] = True
            context['add_url'] = 'centros_de_salud.servicios.create'
        return context


class ServicioCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = Servicio
    permission_required = ("view_servicio",)
    fields = ['centro', 'especialidad']
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'centros_de_salud.servicios'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.servicios"
        )


class ServicioDetailView(PermissionRequiredMixin, DetailView):
    model = Servicio
    permission_required = ("view_servicio",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'centros_de_salud.servicios'
        return context


class ServicioUpdateView(PermissionRequiredMixin, UpdateView):
    model = Servicio
    permission_required = "change_servicio"
    fields = ['centro', 'especialidad']
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de prestacion'
        context['title_url'] = 'centros_de_salud.servicios'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.servicios"
        )