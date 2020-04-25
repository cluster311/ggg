from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.conf import settings
from django.urls import reverse
from .models import CentroDeSalud
from .forms import CentroDeSaludForm


class CentroDeSaludListView(PermissionRequiredMixin, ListView):
    model = CentroDeSalud
    permission_required = ("centros_de_salud.view_centrodesalud",)
    paginate_by = 10  # pagination

    def get_queryset(self):
        """ mostrar todos los centros y permitir 
            modificar solo sobre los cuales tiene permiso
        csp = self.request.user.centros_de_salud_permitidos.all()
        permitidos = [c.centro_de_salud.id for c in csp]
        qs = CentroDeSalud.objects.filter(pk__in=permitidos)
        """
        qs = CentroDeSalud.objects.all()
            
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(codigo_hpgd__icontains=q)
                )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        context['title'] = 'Lista de Centros de salud'
        context['title_url'] = 'centros_de_salud.lista'
        context['use_search_bar'] = True
        if self.request.user.has_perm('centros_de_salud.add_centrodesalud'):
            context['use_add_btn'] = True
            context['add_url'] = 'centros_de_salud.create'
        return context


class CentroDeSaludCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = CentroDeSalud
    permission_required = ("centros_de_salud.add_centrodesalud",)
    form_class = CentroDeSaludForm
    success_message = "Creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Centros de Salud'
        context['subtitle'] = 'Nuevo centro de salud'
        context['title_url'] = 'centros_de_salud.lista'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.lista"
        )

class CentroDeSaludUpdateView(PermissionRequiredMixin, UpdateView):
    model = CentroDeSalud
    permission_required = "centros_de_salud.change_centrodesalud"
    form_class = CentroDeSaludForm
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Centros de Salud'
        context['subtitle'] = 'Editar centro de salud'
        context['title_url'] = 'centros_de_salud.lista'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.lista"
        )


class CentroDeSaludDetailView(PermissionRequiredMixin, DetailView):
    model = CentroDeSalud
    permission_required = ("centros_de_salud.view_centrodesalud",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Centros de Salud'
        context['title_url'] = 'centros_de_salud.lista'
        context['GOOGLE_API_LEY'] = settings.GOOGLE_API_KEY
        return context
