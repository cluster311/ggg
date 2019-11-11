from datetime import datetime, timedelta
from django import forms
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_datetime
import json
from calendario.models import Turno
from calendario.forms import BulkTurnoForm, FeedForm, TurnoForm
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import permission_required


def index(request):
    user = request.user
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
        'form': TurnoForm(user=user)
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
        start=c_start.strftime('%Y-%m-%d %H:%M:%S'),
        end=c_end.strftime('%Y-%m-%d %H:%M:%S')
    )
    appointments = get_appointments_list(
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


def feed(request):
    turnos = get_appointments_list(**request.GET)
    turnos = [{
        'id': t.id,
        'title': str(t),
        'start': t.inicio.isoformat(),
        'end': t.fin.isoformat(),
        'service': t.servicio.pk or 0,
        'status': t.estado,
        'professional': t.profesional.pk or 0,
        # 'patient': t.paciente.pk or 0
    } for t in turnos]

    return JsonResponse(turnos, safe=False)


def get_appointments_list(**kwargs):
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
    return Turno.objects.filter(**kw)
