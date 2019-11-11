from django.conf import settings
from centros_de_salud.models import CentroDeSalud


def cpp_usuarios(request):
    user = request.user
    if user.is_superuser:
        centros_de_salud_permitidos = CentroDeSalud.objects.all()
    else:
        centros_de_salud_permitidos = user.centros_de_salud_permitidos.all()

    context = {}
    context["user__centros_de_salud_autorizados"] = centros_de_salud_permitidos

    context["user__es_ciudadno"] = user.groups.filter(name=settings.GRUPO_CIUDADANO).exists()
    context["user__es_administrativo"] = user.is_superuser or user.groups.filter(name=settings.GRUPO_ADMIN).exists()
    context["user__es_profesional"] = user.groups.filter(name=settings.GRUPO_PROFESIONAL).exists()
    
    return context