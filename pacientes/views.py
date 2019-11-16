from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.conf import settings
from .models import Consulta
from .forms import (EvolucionForm, ConsultaForm,
                   RecetaFormset, DerivacionFormset, 
                   PrestacionFormset)
from crispy_forms.utils import render_crispy_form
import logging
logger = logging.getLogger(__name__)


class ConsultaListView(PermissionRequiredMixin, ListView):
    """
    Lista de consultas de un paciente para la interfaz del profesional.
    """

    model = Consulta
    permission_required = ("can_view_tablero",)
    template_name = "pacientes/consulta_listview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dni = self.kwargs["dni"]
        consultas = Consulta.objects.filter(paciente__numero_documento=dni)
        context["consultas"] = consultas

        return context


class ConsultaDetailView(PermissionRequiredMixin, DetailView):
    """
    Detalle de un objeto Consulta
    """

    model = Consulta
    permission_required = ("can_view_tablero",)
    template_name = "pacientes/consulta_detailview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = self.object.created.strftime("%d/%m/%Y")

        return context


class ConsultaMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = getattr(self, 'object', None)
        
        data = self.request.POST if self.request.method == "POST" else None
        
        context["recetas_frm"] = RecetaFormset(data, prefix='Recetas', instance=instance)
        context["derivaciones_frm"] = DerivacionFormset(data, prefix='Derivaciones', instance=instance)
        context["prestaciones_frm"] = PrestacionFormset(data, prefix='Prestaciones', instance=instance)
       
        context["formsets"] = [
            context["recetas_frm"],
            context["derivaciones_frm"],
            context["prestaciones_frm"]
        ]        

        # se requieren las consultas anteriores como historia clínica
        if instance is None or instance.paciente is None:
            context['consultas_previas'] = None
        else:
            consultas_previas = Consulta.objects.filter(
                paciente=instance.paciente
                )
            context['consultas_previas'] = consultas_previas
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        
        rs = context["recetas_frm"]
        ds = context["derivaciones_frm"]
        ps = context["prestaciones_frm"]

        self.object = form.save()
        
        if rs.is_valid():
            rs.instance = self.object
            rs.save()
        
        if ds.is_valid():
            ds.instance = self.object
            ds.save()
        
        if ps.is_valid():
            ps.instance = self.object
            ps.save()
        
        return super().form_valid(form)


class EvolucionCreateView(ConsultaMixin, SuccessMessageMixin, 
                          PermissionRequiredMixin,
                          CreateView, ):
    """Evolución /Consulta de paciente"""

    permission_required = ("add_consulta",)
    template_name = "pacientes/evolucion_create.html"
    form_class = EvolucionForm
    success_message = "Datos guardados con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evolución Paciente'
        return context

    def get_success_url(self):
        return reverse(
            "pacientes.consulta.lista",
            kwargs=({"dni": self.object.paciente.numero_documento}),
        )


class ConsultaCreateView(ConsultaMixin, SuccessMessageMixin, PermissionRequiredMixin,
                         CreateView, ):
    """Crea un objeto Consulta."""

    permission_required = ("can_view_tablero",)
    template_name = "pacientes/consulta_createview.html"
    form_class = ConsultaForm
    success_message = "Datos guardados con éxito."

    def get_success_url(self):
        return reverse(
            "pacientes.consulta.lista",
            kwargs=({"dni": self.object.paciente.numero_documento}),
        )


class ConsultaUpdateView(ConsultaMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """
    Actualiza un objeto Consulta
    """

    model = Consulta
    form_class = ConsultaForm
    permission_required = ("can_view_tablero",)
    
    template_name = "pacientes/consulta_updateview.html"
    success_message = "Datos actualizados con éxito."

    
    def get_object(self):
        return get_object_or_404(Consulta, 
            paciente__numero_documento=self.kwargs.get('dni'),
            pk=self.kwargs.get('pk')
        ) 

    def get_success_url(self):
        return reverse(
            "pacientes.consulta.lista",
            kwargs=({"dni": self.object.paciente.numero_documento}),
        )

