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
    permission_required = ("recupero.view_tipodocumentoanexo",)
    raise_exception = True
    paginate_by = 10

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
        context['title'] = 'Tipos de documentos anexos'
        context['title_url'] = 'recupero.tipos-doc-anexo'
        context['use_search_bar'] = True
        if self.request.user.has_perm('recupero.add_tipodocumentoanexo'):
            context['use_add_btn'] = True
            context['add_url'] = 'recupero.tipos-documento-anexo.create'
        return context


class TipoDocumentoAnexoCreateView(PermissionRequiredMixin,
                                   CreateView,
                                   SuccessMessageMixin):
    model = TipoDocumentoAnexo
    permission_required = ("recupero.add_tipodocumentoanexo",)
    fields = ['nombre']
    success_message = "Creado con éxito."
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de documentos anexos'
        context['title_url'] = 'recupero.tipos-doc-anexo'
        return context

    def get_success_url(self):
        return reverse(
            "recupero.tipos-doc-anexo"
        )


class TipoDocumentoAnexoDetailView(PermissionRequiredMixin, DetailView):
    model = TipoDocumentoAnexo
    permission_required = ("recupero.view_tipodocumentoanexo",)
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de documentos anexos'
        context['title_url'] = 'recupero.tipos-doc-anexo'
        return context


class TipoDocumentoAnexoUpdateView(PermissionRequiredMixin, UpdateView):
    model = TipoDocumentoAnexo
    permission_required = "recupero.change_tipodocumentoanexo"
    fields = ['nombre']
    success_message = "Actualizado con éxito."
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de documentos anexos'
        context['title_url'] = 'recupero.tipos-doc-anexo'
        return context

    def get_success_url(self):
        return reverse(
            "recupero.tipos-doc-anexo"
        )
