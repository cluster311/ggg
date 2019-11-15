from braces.views import GroupRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.conf import settings
from calendario.models import Turno

class LandingPage(TemplateView):
    """Landing page del sistema """
    template_name = "landing.html"


class CiudadanoHome(TemplateView):
    """ Definir la home del ciudadano """
    template_name = "home-ciudadano.html"


class ProfesionalHome(TemplateView, GroupRequiredMixin):
    """
    Home del profesional al loguearse
    """

    group_required = (settings.GRUPO_PROFESIONAL,)
    template_name = "home_profesional.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # asegurarse de que el turno tenga medico y paciente asignado!
        context['turnos'] = Turno.objects.all()

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['search_txt'] = self.request.GET.get('search', '')
    #     context['title'] = 'Lista de profesionales'
    #     context['title_url'] = 'profesionales.lista'
    #     context['use_search_bar'] = True
    #     if self.request.user.has_perm('profesionales.add_profesional'):
    #         context['use_add_btn'] = True
    #         context['add_url'] = 'profesionales.create'
    #     return context


@login_required
def choice_homepage(request):
    """
    redirige a un dashboard distinto en funcion del tipo de usuario
    """
    user = request.user

    # todo usuario pertenece al grupo ciudano
    if (user.groups.filter(name=settings.GRUPO_PROFESIONAL).exists() and
        user.groups.filter(name=settings.GRUPO_CIUDADANO).exists()):
        return redirect('profesionales.home')
    elif (user.groups.filter(name=settings.GRUPO_ADMIN).exists() and
    user.groups.filter(name=settings.GRUPO_CIUDADANO).exists()):
        return redirect('calendario.index')
    else:
        return redirect('ciudadano.home')

    # default para ciudadano  
    # TODO. cual es el home para el ciudadano?   
    # return redirect('ciudadano.home')

