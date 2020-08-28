from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Count, Q, F
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin

from .forms import FacturaForm, FacturaPrestacionFormSet
from .models import Factura, TipoDocumentoAnexo, TipoPrestacion


class FacturaListView(PermissionRequiredMixin, ListView):
    """
    Lista de facturas de recupero
    """
    template_name = 'recupero/factura_list.html'
    model = Factura
    permission_required = ("recupero.view_factura",)
    paginate_by = 10  # pagination
    raise_exception = True

    def get_queryset(self):
        objects = Factura.objects.all()
        if 'obra-social' in self.request.GET:
            q = self.request.GET['obra-social']
            if not q == '---':
                objects = objects.filter(obra_social_id=q)
        if 'centro-salud' in self.request.GET:
            q = self.request.GET['centro-salud']
            if not q == '---':
                objects = objects.filter(consulta__centro_de_salud__id=q)
        if 'especialidad' in self.request.GET:
            q = self.request.GET['especialidad']
            if not q == '---':
                objects = objects.filter(consulta__especialidad__id=q)
        if 'estado' in self.request.GET:
            q = self.request.GET['estado']
            if not q == '---':
                objects = objects.filter(estado=q)
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            objects = objects.filter(
                Q(consulta__especialidad__nombre__icontains=q) |
                Q(consulta__codigo_cie_principal__code__icontains=q) |
                Q(consulta__profesional__nombres__icontains=q) |
                Q(consulta__centro_de_salud__nombre__icontains=q) |
                Q(obra_social__nombre__icontains=q)
                )
        # Excluir las facturas nuevas y ordernar por últimas modificadas
        objects = objects.exclude(estado=Factura.EST_NUEVO).order_by('-modified')
        return objects
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facturas de recupero'
        context['title_url'] = 'recupero.facturas'
        context['search_txt'] = self.request.GET.get('search', '')
        context['use_search_bar'] = True
        context['use_filter_bar'] = True
        if self.request.user.has_perm('recupero.add_factura'):
            context['use_add_btn'] = True
            context['add_url'] = 'recupero.factura.create'
        context['obra_sociales'] = Factura.objects.filter(obra_social__isnull=False).annotate(identificador=F('obra_social__id'), valor=F('obra_social__siglas')).values('identificador', 'valor').distinct()
        context['centro_de_salud'] = Factura.objects.all().annotate(identificador=F('consulta__centro_de_salud__id'), valor=F('consulta__centro_de_salud__nombre')).values('identificador', 'valor').distinct()
        context['especialidad'] = Factura.objects.all().annotate(identificador=F('consulta__especialidad__id'), valor=F('consulta__especialidad__nombre')).values('identificador', 'valor').distinct()
        context['estado'] = Factura.objects.all().annotate(identificador=F('estado'), valor=F('estado')).values('identificador', 'valor').distinct()
        for c in context['estado']:
            c['valor'] = dict(Factura.estados)[c['valor']]
        filter = []
        filter_txt = ''
        if len(context['obra_sociales']) > 0:
            get_obra_social = self.request.GET.get('obra-social', '',)
            if get_obra_social and not get_obra_social == '---':
                filter_txt += '&obra-social=' + str(get_obra_social)
                filter.append(('obra-social', 'Obra Social', context['obra_sociales'], str(get_obra_social)))
            else:
                filter.append(('obra-social', 'Obra Social', context['obra_sociales'], None))
        if len(context['centro_de_salud']) > 0:
            get_centro_salud = self.request.GET.get('centro-salud', '', )
            if get_centro_salud and not get_centro_salud == '---':
                filter_txt += '&centro-salud=' + str(get_centro_salud)
                filter.append(('centro-salud', 'Centro de salud', context['centro_de_salud'], get_centro_salud))
            else:
                filter.append(('centro-salud', 'Centro de salud', context['centro_de_salud'], None))
        if len(context['especialidad']) > 0:
            get_especialidad = self.request.GET.get('especialidad', '', )
            if get_especialidad and not get_especialidad == '---':
                filter_txt += '&especialidad=' + str(get_especialidad)
                filter.append(('especialidad', 'Especialidad', context['especialidad'], get_especialidad))
            else:
                filter.append(('especialidad', 'Especialidad', context['especialidad'], None))
        if len(context['estado']) > 0:
            get_estado = self.request.GET.get('estado', '', )
            if get_estado and not get_estado == '---':
                filter_txt += '&estado=' + str(get_estado)
                filter.append(('estado', 'Estado', context['estado'], get_estado))
            else:
                filter.append(('estado', 'Estado', context['estado'], None))
        context['filters'] = filter
        context['filter_txt'] = filter_txt
        return context


class FacturaCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    model = Factura
    permission_required = ("recupero.add_factura",)
    success_message = "Creado con éxito."
    template_name = "recupero/factura_create_form.html"
    raise_exception = True
    form_class = FacturaForm

    def get_form_kwargs(self):
        kwargs = super(FacturaCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(FacturaCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Facturas de rcupero'
        context['title_url'] = 'recupero.facturas'
        if self.request.POST:
            context['prestaciones'] = FacturaPrestacionFormSet(self.request.POST)
        else:
            context['prestaciones'] = FacturaPrestacionFormSet()
        return context

    def get_success_url(self):
        return reverse(
            "recupero.facturas"
        )

    def form_valid(self, form):
        context = self.get_context_data()
        fp = context["prestaciones"]
        self.object = form.save()
        if fp.is_valid():
            fp.instance = self.object
            fp.save()
        return super(FacturaCreateView, self).form_valid(form)


class FacturaDetailView(PermissionRequiredMixin, DetailView):
    model = Factura
    permission_required = ("recupero.view_factura",)
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestaciones'] = FacturaPrestacionFormSet()
        context['title'] = 'Factura de recupero'
        context['title_url'] = 'recupero.facturas'
        return context


class FacturaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Factura
    permission_required = "recupero.change_factura"
    form_class = FacturaForm
    template_name = "recupero/factura_create_form.html"
    success_message = "Actualizado con éxito."
    raise_exception = True

    def get_form_kwargs(self):
        kwargs = super(FacturaUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = getattr(self, 'object', None)
        if self.request.POST:
            context['prestaciones'] = FacturaPrestacionFormSet(self.request.POST, instance=self.object)
        else:
            context['prestaciones'] = FacturaPrestacionFormSet(instance=self.object)
        context['title'] = 'Factura de recupero'
        context['title_url'] = 'recupero.facturas'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        fp = context["prestaciones"]
        self.object = form.save()
        if fp.is_valid():
            fp.instance = self.object
            fp.save()
        return super(FacturaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "recupero.facturas"
        )
