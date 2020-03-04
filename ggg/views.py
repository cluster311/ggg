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

class RecuperoHome(TemplateView):
    """ Definir la home del usuario de recupero """
    template_name = "home-recupero.html"

class SuperAdminHome(TemplateView):
    """ Definir la home del usuario superadministrador """
    template_name = "home-super.html"

class DataHome(TemplateView):
    """ Definir la home del analista de datos """
    template_name = "home-data.html"


@login_required
def choice_homepage(request):
    """
    redirige a un dashboard distinto en funcion del tipo de usuario
    """
    user = request.user
    es_profesional = user.groups.filter(name=settings.GRUPO_PROFESIONAL).exists()
    # es_ciudadano = user.groups.filter(name=settings.GRUPO_CIUDADANO)
    es_administrativo = user.groups.filter(name=settings.GRUPO_ADMIN)
    es_data = user.groups.filter(name=settings.GRUPO_DATOS)
    es_super = user.groups.filter(name=settings.GRUPO_SUPER_ADMIN)
    es_recupero = user.groups.filter(name=settings.GRUPO_RECUPERO)

    # todo usuario pertenece al grupo ciudano
    if es_super:
        return redirect('super.home')
    elif es_profesional:
        return redirect('profesionales.home')
    elif es_administrativo:
        return redirect('calendario.index')
    elif es_recupero:
        return redirect('recupero.home')
    elif es_data:
        return redirect('data.home')
    else:
        return redirect('ciudadano.home')