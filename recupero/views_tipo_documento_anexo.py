from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from crispy_forms.utils import render_crispy_form

from .models import TipoDocumentoAnexo


class TipoDocumentoAnexoListView(PermissionRequiredMixin, ListView):
    """
    Lista de tipos de prestaciones habilitadas para recuperar
    """
    model = TipoDocumentoAnexo
    permission_required = ("view_tipodocumentoanexo",)
    paginate_by = 15

    def get_queryset(self):   
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = TipoDocumentoAnexo.objects.filter(
                nombre__icontains=q)
        else:
            objects = TipoDocumentoAnexo.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        return context


class TipoDocumentoAnexoCreateView(PermissionRequiredMixin,
                                   CreateView,
                                   SuccessMessageMixin):
    model = TipoDocumentoAnexo
    permission_required = ("view_tipodocumentoanexo",)
    fields = ['nombre']
    success_message = "Creado con éxito."

    def get_success_url(self):
        return reverse(
            "recupero.tipos-doc-anexo"
        )


class TipoDocumentoAnexoDetailView(PermissionRequiredMixin, DetailView):
    model = TipoDocumentoAnexo
    permission_required = ("view_tipodocumentoanexo",)


class TipoDocumentoAnexoUpdateView(PermissionRequiredMixin, UpdateView):
    model = TipoDocumentoAnexo
    permission_required = "change_tipodocumentoanexo"
    fields = ['nombre']
    success_message = "Actualizado con éxito."

    def get_success_url(self):
        return reverse(
            "recupero.tipos-doc-anexo"
        )