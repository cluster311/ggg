from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from .models import CentroDeSalud


@method_decorator(cache_page(60 * 5), name='dispatch')
class CentroDeSaludListView(PermissionRequiredMixin, ListView):
    model = CentroDeSalud
    permission_required = ("view_centrodesalud",)
    paginate_by = 10  # pagination

    def get_queryset(self):        
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = CentroDeSalud.objects.filter(
                Q(nombre__icontains=q) |
                Q(codigo_hpgd__icontains=q)
                )
        else:
            objects = CentroDeSalud.objects.all()
        
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_txt'] = self.request.GET.get('search', '')
        return context
