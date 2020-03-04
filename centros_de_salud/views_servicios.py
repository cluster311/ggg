from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from crispy_forms.utils import render_crispy_form

from .models import Servicio, CentroDeSalud, Especialidad
from .forms import ServicioForm


class ServicioListView(PermissionRequiredMixin, ListView):
    """
    Lista de Servicios
    """
    model = Servicio
    permission_required = ("centros_de_salud.view_servicio",)
    paginate_by = 10

    def get_queryset(self):
        csp = self.request.user.centros_de_salud_permitidos.all()
        permitidos = [c.centro_de_salud for c in csp]
        qs = Servicio.objects.filter(centro__in=permitidos)

        if 'search' in self.request.GET:
            q = self.request.GET['search']
            qs = qs.filter(
                Q(centro__nombre__icontains=q) |
                Q(especialidad__nombre__icontains=q)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Servicios'
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
    permission_required = ("centros_de_salud.view_servicio",)
    success_message = "Creado con éxito."
    form_class = ServicioForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Servicios'
        context['title_url'] = 'centros_de_salud.servicios'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.servicios"
        )


class ServicioDetailView(PermissionRequiredMixin, DetailView):
    model = Servicio
    permission_required = ("centros_de_salud.view_servicio",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Servicios'
        context['title_url'] = 'centros_de_salud.servicios'
        return context


class ServicioUpdateView(PermissionRequiredMixin, UpdateView):
    model = Servicio
    permission_required = "centros_de_salud.change_servicio"
    success_message = "Actualizado con éxito."
    form_class = ServicioForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Servicios'
        context['title_url'] = 'centros_de_salud.servicios'
        return context

    def get_success_url(self):
        return reverse(
            "centros_de_salud.servicios"
        )


@permission_required('calendario.can_schedule_turno')
@require_http_methods(["GET"])
def servicios_by_especialidad(request, pk):
    instance = get_object_or_404(Especialidad, id=pk)
    servicios = Servicio.objects.filter(especialidad=instance)
    data = {'results': [] }
    for servicio in servicios:
        data['results'].append({
            'id': servicio.pk,
            'text': servicio.centro.nombre
        })
    return JsonResponse(data)