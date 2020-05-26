import json
from django.core.exceptions import PermissionDenied
from calendario.models import Turno
from centros_de_salud.models import Servicio


def centro_de_salud_habilitado_form(function):
    '''Decorador para asegurarse que un formulario X no pueda ejecutar su operación
       si no tiene permiso el usuario Y, esta implementacion sirve mas para los CREATE
    '''
    def _inner(request, *args, **kwargs):
        centro = Servicio.objects.get(id=json.loads(request.body)['servicio']).centro
        if request.user.centros_de_salud_permitidos.filter(centro_de_salud=centro).exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("No tiene permiso para actuar en este centro de salud")

    return _inner


def centro_de_salud_habilitado_pk(function):
    '''Decorador para asegurarse que un formulario X no pueda ejecutar su operación
       si no tiene permiso el usuario Y, esta implementacion sirve mas para las operaciones UPDATE, DELETE
    '''
    def _inner(request, *args, **kwargs):
        turno = Turno.objects.select_related('servicio').get(id=kwargs['pk'])
        centro = turno.servicio.centro
        if request.user.centros_de_salud_permitidos.filter(centro_de_salud=centro).exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("No tiene permiso para actuar en este centro de salud")

    return _inner
