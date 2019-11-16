from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from .forms import MedidasAnexasEspecialidadForm
from .models import MedidasAnexasEspecialidad


class MedidasAnexasEspecialidadListView(PermissionRequiredMixin, ListView):
    """
    Lista de Profesionales en Servicios
    """
    model = MedidasAnexasEspecialidad
    permission_required = ("view_medidasanexasespecialidad",)
    paginate_by = 10

    def get_queryset(self):

        qs = MedidasAnexasEspecialidad.objects.all()

        if 'search' in self.request.GET:
            q = self.request.GET['search']
            qs = qs.filter(
                Q(especialidad__nombre__icontains=q) |
                Q(medida__nombre__icontains=q)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Medidas Anexas en Especialidades'
        context['title_url'] = 'especialidades.medidas-anexas-en-especialidades'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('especialidades.add_medidasanexasespecialidad'):
            context['use_add_btn'] = True
            context['add_url'] = 'especialidades.medidas-anexas-en-especialidades.create'
        return context


class MedidasAnexasEspecialidadCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = MedidasAnexasEspecialidad
    permission_required = ("view_medidasanexasespecialidad",)
    form_class = MedidasAnexasEspecialidadForm
    success_message = "Creado con éxito."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Medidas Anexas en Especialidades'
        context['title_url'] = 'especialidades.medidas-anexas-en-especialidades'
        return context

    def get_success_url(self):
        return reverse(
            "especialidades.medidas-anexas-en-especialidades"
        )


class MedidasAnexasEspecialidadDetailView(PermissionRequiredMixin, DetailView):
    model = MedidasAnexasEspecialidad
    permission_required = ("view_medidasanexasespecialidad",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Medidas Anexas en Especialidades'
        context['title_url'] = 'especialidades.medidas-anexas-en-especialidades'
        return context


class MedidasAnexasEspecialidadUpdateView(PermissionRequiredMixin, UpdateView):
    model = MedidasAnexasEspecialidad
    permission_required = "change_medidasanexasespecialidad"
    form_class = MedidasAnexasEspecialidadForm
    success_message = "Actualizado con éxito."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Medidas Anexas en Especialidades'
        context['title_url'] = 'especialidades.medidas-anexas-en-especialidades'
        return context

    def get_success_url(self):
        return reverse(
            "especialidades.medidas-anexas-en-especialidades"
        )