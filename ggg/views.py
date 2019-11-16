from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf import settings


class LandingPage(TemplateView):
    """Landing page del sistema """
    template_name = "landing.html"


class CiudadanoHome(TemplateView):
    """ Definir la home del ciudadano """
    template_name = "home-ciudadano.html"


@login_required
def choice_homepage(request):
    """
    redirige a un dashboard distinto en funcion del tipo de usuario
    """
    user = request.user
    if user.groups.filter(name=settings.GRUPO_CIUDADANO).exists():
        return redirect('ciudadano.home')
    elif user.groups.filter(name=settings.GRUPO_ADMIN).exists():
        return redirect('calendario.index')
    elif user.groups.filter(name=settings.GRUPO_PROFESIONAL).exists():
        # TODO cambiar por la nueva vista para atender turnos
        return redirect('profesionales.lista')

    # default para ciudadano  
    # TODO. cual es el home para el ciudadano?   
    return redirect('ciudadano.home')

