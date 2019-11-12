from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from .models import UsuarioEnCentroDeSalud
import logging
logger = logging.getLogger(__name__)


# ya se fija en los centros de salud que tiene permitidos
# @permission_required('')
@require_http_methods(['POST'])
def elegir_centro(request):
    user = request.user
    centro_id = request.POST['centro_id']

    centro = user.centros_de_salud_permitidos.filter(centro_de_salud=centro_id).first()
    if centro is None:
        logger.error(f'Usuario {user} trata de seleccionar el centro {centro_id} no permitido')
        return HttpResponse('Centro de salud no permitido', status=403)
    
    ret = centro.elegir()  # si es falso es porque quizas ya estaba elegido de antes
    
    return JsonResponse({'Centro de salud elegido': ret})

