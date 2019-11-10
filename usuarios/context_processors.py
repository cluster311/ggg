from django.conf import settings
from centros_de_salud.models import CentroDeSalud


def cpp_usuarios(request):
    user = request.user
    if user.is_superuser:
        centros_de_salud_permitidos = CentroDeSalud.objects.all()
    else:
        centros_de_salud_permitidos = user.centros_de_salud_permitidos.all()

    context = {}
    context["centros_de_salud_autorizados"] = centros_de_salud_permitidos
    
    return context