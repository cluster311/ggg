from datetime import datetime, timedelta
from django import forms
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
import json
from calendario.models import Turno
from calendario.forms import BulkTurnoForm, FeedForm, TurnoForm
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import permission_required
from centros_de_salud.models import Servicio, Especialidad
from pacientes.models import Paciente
from obras_sociales.models import ObraSocial


def index(request):
    context = {
        'modal_title': 'Agregar turno',
        'modal_close': 'Cancelar',
        'modal_body_include': 'calendario/add_appointment_form.html',
        'modal_size': 'modal-lg',
        'modal_buttons': (
            '<button type="button" class="btn btn-success" '
            'id="addAppointmentButton" '
            'onclick="customAppointmentFormSubmit();">Agregar</button>'
            '<button type="button" class="btn btn-primary" '
            'id="copyAppointmentButton" '
            'onclick="copyPreviousWeek()">Copiar turnos de la semana anterior</button>'
        ),
        'form': TurnoForm(user=request.user),
        'turno_states': {
            'DISPONIBLE': Turno.DISPONIBLE,
            'ASIGNADO': Turno.ASIGNADO,
            'ESPERANDO_EN_SALA': Turno.ESPERANDO_EN_SALA,
            'ATENDIDO': Turno.ATENDIDO,
            'CANCELADO_PACIENTE': Turno.CANCELADO_PACIENTE,
            'CANCELADO_ESTABLECIMIENTO': Turno.CANCELADO_ESTABLECIMIENTO
        }
    }
    return render(request, 'calendario.html', context)


@permission_required('calendario.add_turno')
def add_appointment(request):
    form_data = json.loads(request.body)
    if form_data['bulk']:
        form = BulkTurnoForm(form_data)
    elif form_data['id']:
        instance = Turno.objects.get(pk=form_data['id'])
        if form_data['delete']:
            instance.delete()
            form = None
        else:
            form = TurnoForm(form_data, instance=instance)
    else:
        form = TurnoForm(form_data)

    if form is None:
        response_data = {'success': True, 'appointments': []}
    elif form.is_valid():
        appointments = form.save()
        if not isinstance(appointments, list):
            appointments = [appointments]
        response_data = {
            'success': True,
            'appointments': [{
                'id': a.id,
                'title': str(a),
                'start': a.inicio.isoformat(),
                'end': a.fin.isoformat(),
            } for a in appointments]
        }
    else:
        logger.error(f'Error al grabar turnos: {form.errors}, data: {form_data}')
        response_data = {'success': False, 'errors': form.errors}

    return JsonResponse(response_data)


@permission_required('calendario.add_turno')
@require_http_methods(["POST"])
def copy_appointments(request):
    form_data = json.loads(request.body)

    sourceInitDate = parse_datetime(form_data['sourceDate'])
    targetInitDate = parse_datetime(form_data['targetDate'])
    servicio = form_data['servicio']

    #Obtener turnos desde el lunes solicitado hasta el viernes
    aweekago_appointments = get_appointments_list(
        user=request.user,
        servicio=servicio,
        start=sourceInitDate.strftime('%Y-%m-%d 00:00:00'),
        end=(sourceInitDate + timedelta(days=4)).strftime('%Y-%m-%d 23:59:59')
    )

    new_appointments = []
    for a in aweekago_appointments:
        #TODO: Chequear si es feriado
        #TODO: Que pasa con los turnos que ya estan creados en la semana target
        a.pk = None
        a.inicio += timedelta(days=7)
        a.fin += timedelta(days=7)
        a.estado = Turno.DISPONIBLE
        a.paciente = None
        a.solicitante = None
        a.save()
        new_appointments.append(a)
    
    response_appointments = [{
        'id': a.id,
        'title': str(a),
        'start': a.inicio.isoformat(),
        'end': a.fin.isoformat(),
    } for a in aweekago_appointments]

    return JsonResponse({
        'success': True,
        'appointments': response_appointments}
    )


def feed(request, servicio=None):
    turnos = get_appointments_list(
        user=request.user, servicio=servicio, estado=Turno.DISPONIBLE, **request.GET)
    turnos = [{
        'id': t.id,
        'title': str(t),
        'start': t.inicio.isoformat(),
        'end': t.fin.isoformat(),
        'service': t.servicio.pk or 0,
        'status': t.estado,
        'professional': t.profesional.pk or 0,
        'patient': t.paciente.as_json() if t.paciente else 0
        # 'patient': t.paciente.pk or 0
    } for t in turnos]

    return JsonResponse(turnos, safe=False)


def get_appointments_list(user, servicio = None, estado = None, **kwargs):
    if 'id' in kwargs:
        pk = kwargs['id'][0] if isinstance(kwargs['id'], list) else \
             kwargs['id']
        return [get_object_or_404(Turno, pk=pk)]
    kw = {}
    if 'start' in kwargs:
        start = kwargs['start'][0] if isinstance(kwargs['start'], list) else \
                kwargs['start']
        kw['inicio__gte'] = parse_datetime(start)
    if 'end' in kwargs:
        end = kwargs['end'][0] if isinstance(kwargs['end'], list) else \
              kwargs['end']
        kw['fin__lte'] = parse_datetime(end)
    if estado is not None:
        kw['estado'] = estado
    if servicio is not None:
        kw['servicio__pk'] = servicio
        return Turno.objects.filter(**kw)
    else:
        csp = user.centros_de_salud_permitidos.all()
        centros_de_salud_permitidos = [c.centro_de_salud for c in csp]
        
        return Turno.objects.filter(servicio__centro__in=centros_de_salud_permitidos, **kw)


@permission_required('calendario.can_schedule_turno')
@require_http_methods(["GET"])
def agendar(request):
    context = {
        'especialidades': Especialidad.objects.all(),
        'sys_logo': settings.SYS_LOGO
    }
    return render(request, 'calendario-agregar.html', context)


@permission_required('calendario.can_schedule_turno')
@require_http_methods(["PUT"])
def confirm_turn(request, pk):
    instance = get_object_or_404(Turno, id=pk)
    form_data = json.loads(request.body)
    form_data['solicitante'] = request.user
    form = TurnoForm(form_data, instance=instance)
    save, result = form.update(form_data)
    if save:
        return JsonResponse({
            'success': save,
            'turno': instance.as_json()}
        )
    else:
        return JsonResponse({
            'success': save,
            'errors': result}
        )


@permission_required('calendario.can_change_turno')
@require_http_methods(["PUT"])
def edit_turn(request, pk):
    instance = get_object_or_404(Turno, id=pk)
    form_data = json.loads(request.body)
    form = TurnoForm(form_data, instance=instance)
    save, result = form.change_state(form_data)
    if save:
        return JsonResponse({
            'success': save,
            'turno': instance.as_json()}
        )
    else:
        return JsonResponse({
            'success': save,
            'errors': result}
        )


@permission_required('calendario.can_view_misturnos')
@require_http_methods(["GET"])
def mis_turnos(request):
    today = datetime.now().replace(hour=0,minute=0,second=0)
    turnos = Turno.objects.filter(
        (Q(solicitante=request.user) | Q(paciente__user=request.user))
        ).filter(inicio__gt=today).order_by('inicio')
    context = {
        'turnos' : turnos,
        'CANCELADO_PACIENTE': Turno.CANCELADO_PACIENTE,
        'CANCELADO_ESTABLECIMIENTO': Turno.CANCELADO_ESTABLECIMIENTO,
    }
    return render(request, 'mis-turnos.html', context)


@permission_required('calendario.can_cancel_turno')
@require_http_methods(["PUT"])
def cancelar_turno(request, pk):
    instance = get_object_or_404(Turno, id=pk)
    form_data = {'state': Turno.CANCELADO_PACIENTE}
    form = TurnoForm(form_data, instance=instance)
    save, result = form.change_state(form_data)
    if save:
        return JsonResponse({
            'success': save,
            'turno': instance.as_json()}
        )
    else:
        return JsonResponse({
            'success': save,
            'errors': result}
        )


@permission_required('calendario.can_gestionar_turnos')
@require_http_methods(["GET"])
def gestion_turnos(request):
    context = {
        'servicios': Servicio.objects.all(),
        'obras_sociales': ObraSocial.objects.all()
    }
    return render(request, 'calendario-gestionar.html', context)


@permission_required('calendario.can_gestionar_turnos')
@require_http_methods(["PUT"])
def gestion_turno(request, pk):
    instance = get_object_or_404(Turno, id=pk)
    form_data = json.loads(request.body)
    logger.info(f'Gestion de turno {pk}: {form_data}')
    form_data['solicitante'] = request.user
    form = TurnoForm(form_data, instance=instance)
    save, result = form.update(form_data)
    if save:
        return JsonResponse({
            'success': save,
            'turno': instance.as_json()}
        )
    else:
        return JsonResponse({
            'success': save,
            'errors': result}
        )