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


@permission_required('calendario.view_turno')
@require_http_methods(["GET"])
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
@require_http_methods(["POST"])
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


def copy_appointments(request):
    if 'start' in request.GET:
        c_start = parse_datetime(request.GET['start'])
    else:
        c_start = datetime.now()
    start = c_start - timedelta(days=7)

    if 'end' in request.GET:
        c_end = parse_datetime(request.GET['end'])
    else:
        c_end = datetime.now() - timedelta(days=1)
    end = c_end - timedelta(days=7)

    current_appointments = get_appointments_list(
        user=request.user,
        start=c_start.strftime('%Y-%m-%d %H:%M:%S'),
        end=c_end.strftime('%Y-%m-%d %H:%M:%S')
    )
    appointments = get_appointments_list(
        user=request.user,
        start=start.strftime('%Y-%m-%d %H:%M:%S'),
        end=end.strftime('%Y-%m-%d %H:%M:%S')
    )

    new_appointments = []
    # TODO: Define what to do with existent appointments
    if c_start != start and c_end != end and len(appointments) > 0:
        current_appointments.delete()

    for a in appointments:
        a.pk = None
        a.inicio += timedelta(days=7)
        a.fin += timedelta(days=7)
        a.save()
        new_appointments.append(a)

    response_appointments = [{
        'id': a.id,
        'title': str(a),
        'start': a.inicio.isoformat(),
        'end': a.fin.isoformat(),
    } for a in appointments]
    return JsonResponse({
        'success': True,
        'appointments': response_appointments}
    )



@permission_required('calendario.view_turno')
@require_http_methods(["GET"])
def feed(request, servicio=None):
    turnos = get_appointments_list(servicio, user=request.user, **request.GET)
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


def get_appointments_list(servicio, user, **kwargs):
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
    if servicio is not None:
        kw['servicio__pk'] = servicio
        kw['estado__in'] = [Turno.DISPONIBLE, Turno.CANCELADO_PACIENTE, Turno.CANCELADO_ESTABLECIMIENTO]
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


@permission_required('calendario.change_turno')
@require_http_methods(["PUT"])
def edit_turn(request, pk):
    # ISSUE asegurarse que el usuario esta activo en el centro de salud donde se hace el cambio
    # https://github.com/cluster311/ggg/issues/181

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

@permission_required('calendario.can_gestionar_turnos')
@require_http_methods(["POST"])
def crear_sobreturno(request, pk):
    instance = get_object_or_404(Turno, id=pk)
    form = TurnoForm({}, instance=instance)
    save, result = form.sobreturno()
    if save:
        return JsonResponse({
            'success': save,
            'turno': result.as_json()}
        )
    else:
        return JsonResponse({
            'success': save,
            'errors': result}
        )
