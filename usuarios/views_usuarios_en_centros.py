from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from crispy_forms.utils import render_crispy_form

from .models import UsuarioEnCentroDeSalud


class UsuarioEnCentroDeSaludListView(PermissionRequiredMixin, ListView):
    """
    Lista de Usuarios en Centros de Salud
    """
    model = UsuarioEnCentroDeSalud
    permission_required = ("view_UsuarioEnCentroDeSalud",)
    paginate_by = 10

    def get_queryset(self):   
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = UsuarioEnCentroDeSalud.objects.filter(
                Q(centro__nombre__icontains=q) |
                Q(especialidad__nombre__icontains=q)
            )
        else:
            objects = UsuarioEnCentroDeSalud.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios en Centros de Salud'
        context['title_url'] = 'usuarios.en-centro-de-salud'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('usuarios.add_usuarioencentrodesalud'):
            context['use_add_btn'] = True
            context['add_url'] = 'usuarios.en-centro-de-salud.create'
        return context


class UsuarioEnCentroDeSaludCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = UsuarioEnCentroDeSalud
    permission_required = ("usuarios.add_usuarioencentrodesalud",)
    fields = ['centro', 'especialidad']
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios en Centros de Salud'
        context['title_url'] = 'usuarios.en-centro-de-salud'
        return context

    def get_success_url(self):
        return reverse(
            "usuarios.en-centro-de-salud"
        )


class UsuarioEnCentroDeSaludDetailView(PermissionRequiredMixin, DetailView):
    model = UsuarioEnCentroDeSalud
    permission_required = ("usuarios.view_usuarioencentrodesalud",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios en Centros de Salud'
        context['title_url'] = 'usuarios.en-centro-de-salud'
        return context


class UsuarioEnCentroDeSaludUpdateView(PermissionRequiredMixin, UpdateView):
    model = UsuarioEnCentroDeSalud
    permission_required = "usuarios.change_usuarioencentrodesalud"
    fields = ['centro', 'especialidad']
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios en Centros de Salud'
        context['title_url'] = 'usuarios.en-centro-de-salud'
        return context

    def get_success_url(self):
        return reverse(
            "usuarios.en-centro-de-salud"
        )