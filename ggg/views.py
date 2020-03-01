from braces.views import GroupRequiredMixin
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


@login_required
def choice_homepage(request):
    """
    redirige a un dashboard distinto en funcion del tipo de usuario
    """
    user = request.user
    es_profesional = user.groups.filter(name=settings.GRUPO_PROFESIONAL).exists()
    # es_ciudadano = user.groups.filter(name=settings.GRUPO_CIUDADANO)
    es_administrativo = user.groups.filter(name=settings.GRUPO_ADMIN)

    # todo usuario pertenece al grupo ciudano
    if es_profesional:
        return redirect('profesionales.home')
    elif es_administrativo:
        return redirect('calendario.index')
    else:
        return redirect('ciudadano.home')