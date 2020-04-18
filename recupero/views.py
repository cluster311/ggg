from django.views.generic.list import ListView
from django.db.models import Count, Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from .models import Factura, TipoDocumentoAnexo, TipoPrestacion


class FacturaListView(PermissionRequiredMixin, ListView):
    """
    Lista de facturas de recupero
    """
    template_name = 'recupero/facturacion-pendiente-de-envio.html'
    model = Factura
    permission_required = ("recupero.change_factura",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            # TODO sumar nombres de OSS, profesionales, CIE secundarios, etc
            objects = Factura.objects.filter(
                Q(especialidad__icontains=q) |
                Q(codigo_cie_principal__icontains=q)
                )
        else:
            #TODO detectar el estado de la factura y listar solo las que esten pendientes
            objects = Factura.objects.all()
        
        return objects


class FacturaPendEnvioView(PermissionRequiredMixin, ListView):
    """
    Lista de facturas pendientes de envio a la OSS para cobro
    """
    template_name = 'recupero/facturacion-pendiente-de-envio.html'
    model = Factura
    permission_required = ("recupero.change_factura",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            # TODO sumar nombres de OSS, profesionales, CIE secundarios, etc
            objects = Factura.objects.filter(
                Q(especialidad__icontains=q) |
                Q(codigo_cie_principal__icontains=q)
                )
        else:
            #TODO detectar el estado de la factura y listar solo las que esten pendientes
            objects = Factura.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        return context


class FacturaPendCobroView(
        PermissionRequiredMixin, ListView):
    """
    Lista de facturas enviadas a las OSS esperando cobrar
    """
    template_name = 'recupero/facturacion-pendiente-de-cobro.html'
    model = Factura
    permission_required = ("recupero.change_factura",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            # TODO sumar nombres de OSS, profesionales, CIE secundarios, etc
            objects = Factura.objects.filter(
                Q(especialidad__icontains=q) |
                Q(codigo_cie_principal__icontains=q)
                )
        else:
            #TODO detectar el estado de la factura y listar solo las que esten pendientes
            objects = Factura.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        return context
