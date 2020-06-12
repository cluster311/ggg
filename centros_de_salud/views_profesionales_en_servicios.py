from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Count, Q, F
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from .forms import ProfesionalesEnServicioForm
from .models import ProfesionalesEnServicio


class ProfesionalesEnServicioListView(PermissionRequiredMixin, ListView):
    '''
        Listado de Servicios ofrecidos por Profesionales

        Grupo acceso disponible: grupo_super_usuario
    '''
    model = ProfesionalesEnServicio
    permission_required = ("centros_de_salud.view_profesionalesenservicio",)
    paginate_by = 10

    def get_queryset(self):
        csp = self.request.user.centros_de_salud_permitidos.all()
        permitidos = [c.centro_de_salud for c in csp]
        qs = ProfesionalesEnServicio.objects.filter(servicio__centro__in=permitidos)

        if 'especialidad' in self.request.GET:
            q = self.request.GET['especialidad']
            if not q == '---':
                qs = qs.filter(servicio__especialidad_id=q)
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
        context['use_filter_bar'] = True
        if self.request.user.has_perm('centros_de_salud.add_profesionalesenservicio'):
            context['use_add_btn'] = True
            context['add_url'] = 'centros_de_salud.profesionales-en-servicio.create'
        csp = self.request.user.centros_de_salud_permitidos.all()
        permitidos = [c.centro_de_salud for c in csp]
        context['especialidad'] = ProfesionalesEnServicio.objects.filter(servicio__centro__in=permitidos).annotate(identificador=F('servicio__especialidad__id'), valor=F('servicio__especialidad__nombre')).values('identificador', 'valor').distinct()
        filter = []
        filter_txt = ''
        if len(context['especialidad']) > 0:
            get_especialidad = self.request.GET.get('especialidad', '',)
            if get_especialidad and not get_especialidad == '---':
                filter_txt += '&especialidad=' + str(get_especialidad)
                filter.append(('especialidad', 'Especialidad', context['especialidad'], str(get_especialidad)))
            else:
                filter.append(('especialidad', 'Especialidad', context['especialidad'], None))
        context['filters'] = filter
        context['filter_txt'] = filter_txt
        return context


class ProfesionalesEnServicioCreateView(PermissionRequiredMixin,
                               CreateView,
                               SuccessMessageMixin):
    '''
        Vista de creación de Servicios ofrecido por Profesionales

        Grupo acceso disponible: grupo_super_usuario
    '''
    model = ProfesionalesEnServicio
    permission_required = ("centros_de_salud.add_profesionalesenservicio",)
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
    '''
        Vista detallada de Servicios ofrecidos por Profesionales

        Grupo acceso disponible: grupo_super_usuario
    '''
    model = ProfesionalesEnServicio
    permission_required = ("centros_de_salud.view_profesionalesenservicio",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profesionales en Servicios'
        context['title_url'] = 'centros_de_salud.profesionales-en-servicio'
        return context


class ProfesionalesEnServicioUpdateView(PermissionRequiredMixin, UpdateView):
    '''
        Vista de actualización de Servicios ofrecido por Profesionales

        Grupo acceso disponible: grupo_super_usuario
    '''
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
