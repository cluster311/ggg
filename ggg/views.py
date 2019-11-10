from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    """Landing page del sistema """
    template_name = "landing.html"


@login_required
def choice_homepage(request):
    """
    redirige a un dashboard distinto en funcion del tipo de usuario
    """
    user = request.user
    if user.groups.filter(name='Municipales').exists():
        return redirect('admin:index')
    elif user.groups.filter(name='Administrativos').exists():
        return redirect('calendario.index')
    elif user.groups.filter(name='Profesionales').exists():
        return redirect('profesionales.crear.consulta')

    # default para ciudadano  
    # TODO. cual es el home para el ciudadano?   
    return redirect('add_appointments')

