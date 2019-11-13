from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.conf import settings


class LandingPage(TemplateView):
    """Landing page del sistema """
    template_name = "landing.html"


class CiudadanoHome(TemplateView):
    """ Definir la home del ciudadano """
    template_name = "home-ciudadano.html"


class ProfesionalHome(TemplateView, PermissionRequiredMixin):
    """
    Home del profesional al loguearse
    """

    # FIXME: Se debería crear otro permiso
    permission_required = ("can_view_tablero",)
    template_name = "home_profesional.html"


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

