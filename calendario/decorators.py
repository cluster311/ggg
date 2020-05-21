import json

from django.core.exceptions import PermissionDenied

from calendario.models import Turno
from centros_de_salud.models import Servicio


def centro_de_salud_habilitado_form(function):

    def _inner(request, *args, **kwargs):
        centro = Servicio.objects.get(id=json.loads(request.body)['servicio']).centro
        if request.user.centros_de_salud_permitidos.filter(centro_de_salud=centro).exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return _inner


def centro_de_salud_habilitado_pk(function):
    def _inner(request, *args, **kwargs):
        turno = Turno.objects.select_related('servicio').get(id=kwargs['pk'])
        centro = turno.servicio.centro
        if request.user.centros_de_salud_permitidos.filter(centro_de_salud=centro).exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return _inner
