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
    permission_required = ("view_tipoprestacion",)
    paginate_by = 15

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
        context['search_txt'] = self.request.GET.get('search', '')
        return context


class TipoPrestacionCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = TipoPrestacion
    permission_required = ("view_tipoprestacion",)
    fields = ['nombre', 'codigo', 'descripcion', 'observaciones',
              'tipo', 'documentos_requeridos', 'documentos_sugeridos']
    success_message = "Creado con éxito."

    def get_success_url(self):
        return reverse(
            "recupero.tipos-prestacion"
        )


class TipoPrestacionDetailView(PermissionRequiredMixin, DetailView):
    model = TipoPrestacion
    permission_required = ("view_tipoprestacion",)


class TipoPrestacionUpdateView(PermissionRequiredMixin, UpdateView):
    model = TipoPrestacion
    permission_required = "change_tipoprestacion"
    fields = ['nombre', 'codigo', 'descripcion', 'observaciones',
              'tipo', 'documentos_requeridos', 'documentos_sugeridos']
    success_message = "Actualizado con éxito."

    def get_success_url(self):
        return reverse(
            "recupero.tipos-prestacion"
        )