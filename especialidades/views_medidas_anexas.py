from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from .models import MedidaAnexa
from .forms import MedidaAnexaForm


class MedidaAnexaListView(PermissionRequiredMixin, ListView):
    """
    Lista de Medidas Anexas
    """
    model = MedidaAnexa
    permission_required = ("view_medidaanexa",)
    paginate_by = 10

    def get_queryset(self):
        qs = MedidaAnexa.objects.all()

        if 'search' in self.request.GET:
            q = self.request.GET['search']
            qs = qs.filter(nombre__icontains=q)
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Medidas Anexas'
        context['title_url'] = 'especialidades.medidas_anexas'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('especialidades.add_medidaanexa'):
            context['use_add_btn'] = True
            context['add_url'] = 'especialidades.medidas_anexas.create'
        return context


class MedidaAnexaCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = MedidaAnexa
    permission_required = ("view_medidaanexa",)
    success_message = "Creado con éxito."
    form_class = MedidaAnexaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MedidaAnexas'
        context['title_url'] = 'especialidades.medidas_anexas'
        return context

    def get_success_url(self):
        return reverse(
            "especialidades.medidas_anexas"
        )


class MedidaAnexaDetailView(PermissionRequiredMixin, DetailView):
    model = MedidaAnexa
    permission_required = ("view_medidaanexa",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MedidaAnexas'
        context['title_url'] = 'especialidades.medidas_anexas'
        return context


class MedidaAnexaUpdateView(PermissionRequiredMixin, UpdateView):
    model = MedidaAnexa
    permission_required = "change_medidaanexa"
    success_message = "Actualizado con éxito."
    form_class = MedidaAnexaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MedidaAnexas'
        context['title_url'] = 'especialidades.medidas_anexas'
        return context

    def get_success_url(self):
        return reverse(
            "especialidades.medidas_anexas"
        )