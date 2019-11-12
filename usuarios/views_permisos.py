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
        
        permisos = [
            {'nombre': 'Obras sociales', 
             'valores': [
                {'nombre': 'Obra Social',
                 'permisos': ['ver', 'cambiar', 'agregar', 'analizar tableros'],
                 'ayuda': 'Lista de Obras Sociales en el sistema'}
                ]
            },
            {'nombre': 'Usuarios', 
             'valores': [
                {'nombre': 'Definir permisos', 'permisos': ['ver', 'cambiar'],
                 'ayuda': 'Definir los permisos de todos los usuarios del sistema. Dejar SOLO a usuarios especializados'},
                {'nombre': 'Asignar a Centro de Salud', 'permisos': ['ver', 'cambiar'],
                 'ayuda': 'Los permisos de cada usuario solo aplican a los centros de salud definidos para el. Los centros de salud donde todos estos permisos funcionarán los definen los usuarios con este permiso.'}
                ]
            },
            {'nombre': 'Pacientes', 
             'valores': [
                {'nombre': 'Paciente', 'permisos': ['cambiar', 'agregar'],
                 'ayuda': 'Nadie puede ver la lista completa de pacientes'},
                {'nombre': 'Consulta', 'permisos': ['ver', 'cambiar', 'agregar']},
                ]
            },
            {'nombre': 'Profesionales', 
             'valores': [
                {'nombre': 'Profesional', 'permisos': ['ver', 'cambiar', 'agregar', 'analizar tableros']},
                {'nombre': 'Profesional en servicio', 'permisos': ['ver', 'cambiar', 'agregar']}
                ]
            },
            {'nombre': 'Centros de Salud', 
             'valores': [
                {'nombre': 'Centro de Salud', 'permisos': ['ver', 'cambiar', 'agregar', 'analizar tableros']},
                {'nombre': 'Especialidad', 'permisos': ['ver', 'cambiar', 'agregar']},
                {'nombre': 'Servicio', 'permisos': ['ver', 'cambiar', 'agregar']},
                {'nombre': 'Turno', 'permisos': ['ver', 'cambiar', 'agregar']}
                ]
            },
            {'nombre': 'Recupero', 
             'valores': [
                {'nombre': 'Prestacion', 'permisos': ['ver', 'cambiar', 'agregar']},
                {'nombre': 'Tipos de Prestacion', 'permisos': ['ver', 'cambiar', 'agregar']},
                {'nombre': 'Tipos de Documentos Anexos', 'permisos': ['ver', 'cambiar', 'agregar']},
                {'nombre': 'Factura a Obra Social', 'permisos': ['ver', 'cambiar', 'agregar']}
                ]
            },
        ]

        # apps = django_apps.get_app_configs()
        # context['apps'] = []
        # for app in apps:
        #     for model in app.get_models():
        #         obj = {
        #             'app_label': app.label,
        #             'app_vn': app.verbose_name.replace('_', ' '),
        #             'name': model.__name__,
        #             'model': model,
        #             'permissions': model._meta.permissions,

        #         }
        #         context['apps'].append(obj)
                
        context['permisos'] = permisos
        return context
