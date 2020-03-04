from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from .forms import ProfesionalesEnServicioForm
from .models import ProfesionalesEnServicio


class ProfesionalesEnServicioListView(PermissionRequiredMixin, ListView):
    """
    Lista de Profesionales en Servicios
    """
    model = ProfesionalesEnServicio
    permission_required = ("centros_de_salud.view_profesionalesenservicio",)
    paginate_by = 10

    def get_queryset(self):

        csp = self.request.user.centros_de_salud_permitidos.all()
        permitidos = [c.centro_de_salud for c in csp]
        qs = ProfesionalesEnServicio.objects.filter(servicio__centro__in=permitidos)

        if 'search' in self.request.GET:
            q = self.request.GET['search']
            qs = qs.filter(
                Q(servicio__centro__nombre__icontains=q) |
                Q(servicio__especialidad__nombre__icontains=q) |
                Q(profesional__apellidos__icontains=q) |
                Q(profesional__nombres__icontains=q)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales en Servicios'
        context['title_url'] = 'centros_de_salud.profesionales-en-servicio'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('centros_de_salud.add_profesionalesenservicio'):
            context['use_add_btn'] = True
            context['add_url'] = 'centros_de_salud.profesionales-en-servicio.create'
        return context


class ProfesionalesEnServicioCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = ProfesionalesEnServicio
    permission_required = ("centros_de_salud.view_profesionalesenservicio",)
    form_class = ProfesionalesEnServicioForm
    success_message = "Creado con éxito."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales en Servicios'
        context['title_url'] = 'centros_de_salud.profesionales-en-servicio'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.profesionales-en-servicio"
        )


class ProfesionalesEnServicioDetailView(PermissionRequiredMixin, DetailView):
    model = ProfesionalesEnServicio
    permission_required = ("centros_de_salud.view_profesionalesenservicio",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales en Servicios'
        context['title_url'] = 'centros_de_salud.profesionales-en-servicio'
        return context


class ProfesionalesEnServicioUpdateView(PermissionRequiredMixin, UpdateView):
    model = ProfesionalesEnServicio
    permission_required = "centros_de_salud.change_profesionalesenservicio"
    form_class = ProfesionalesEnServicioForm
    success_message = "Actualizado con éxito."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales en Servicios'
        context['title_url'] = 'centros_de_salud.profesionales-en-servicio'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.profesionales-en-servicio"
        )