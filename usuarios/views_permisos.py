from django.apps import apps as django_apps
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin


class EditUserPermissionView(PermissionRequiredMixin, TemplateView):
    """
    Lista de permisos de los Usuarios
    """
    permission_required = ("auth.change_user",)
    template_name = 'usuarios/change_user_permission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        availables = [
            'Autenticación y autorización - User', 
            'Obras Sociales - ObraSocial', 
            'Pacientes - CarpetaFamiliar', 
            'Pacientes - Paciente', 
            'Pacientes - Consulta', 
            'Pacientes - Receta', 
            'Pacientes - Derivacion', 
            'Profesionales - Profesional', 
            'Centros De Salud - Institucion', 
            'Centros De Salud - CentroDeSalud', 
            'Centros De Salud - Especialidad', 
            'Centros De Salud - Servicio', 
            'Centros De Salud - ProfesionalesEnServicio', 
            'Calendario - Turno', 
            'Recupero - TipoDocumentoAnexo', 
            'Recupero - TipoPrestacion', 
            'Recupero - Prestacion', 
            'Recupero - DocumentoAnexo', 
            'Recupero - Factura', 
            'Usuarios - UsuarioEnCentroDeSalud'
        ]
        
        apps = django_apps.get_app_configs()
        context['apps'] = []
        for app in apps:
            for model in app.get_models():
                obj = {
                    'app_label': app.label,
                    'app_vn': app.verbose_name.replace('_', ' '),
                    'name': model.__name__,
                    'model': model,
                    'permissions': model._meta.permissions,

                }
                context['apps'].append(obj)
                
        
        # context['apps_apps'] = context['apps'].apps
        # context['modelos'] = context['apps_apps'].get_models()
        return context
