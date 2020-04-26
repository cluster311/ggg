from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Count, Q
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from .models import Factura, TipoDocumentoAnexo, TipoPrestacion


class FacturaListView(PermissionRequiredMixin, ListView):
    """
    Lista de facturas de recupero
    """
    template_name = 'recupero/factura_list.html'
    model = Factura
    permission_required = ("recupero.view_factura",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = Factura.objects.filter(
                Q(consulta__especialidad__nombre__icontains=q) |
                Q(consulta__codigo_cie_principal__code__icontains=q)
                )
        else:
            objects = Factura.objects.all()
        
        # mostrar prinmero los ultimos modificados
        objects = objects.order_by('-modified')
        return objects
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facturas de recupero'
        context['title_url'] = 'recupero.facturas'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        if self.request.user.has_perm('recupero.add_factura'):
            context['use_add_btn'] = True
            context['add_url'] = 'recupero.factura.create'
        return context


class FacturaCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = Factura
    permission_required = ("recupero.add_factura",)
    fields = ['estado', 'obra_social']
    success_message = "Creado con éxito."
    template_name = "recupero/factura_create_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facturas de rcupero'
        context['title_url'] = 'recupero.facturas'
        return context

    def get_success_url(self):
        return reverse(
            "recupero.facturas"
        )

class FacturaDetailView(PermissionRequiredMixin, DetailView):
    model = Factura
    permission_required = ("recupero.view_factura",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura de recupero'
        context['title_url'] = 'recupero.facturas'
        return context


class FacturaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Factura
    permission_required = "recupero.change_factura"
    fields = ['estado', 'obra_social']
    success_message = "Actualizado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura de recupero'
        context['title_url'] = 'recupero.facturas'
        return context

    def get_success_url(self):
        return reverse(
            "recupero.facturas"
        )
