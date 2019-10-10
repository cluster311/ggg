from django import forms
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
import json
from calendario.models import Turno
from calendario.forms import FeedForm, TurnoForm


def index(request):
    context = {
        'modal_title': 'Agregar turno',
        'modal_close': 'Cancelar',
        'modal_body_include': 'calendario/add_appointment_form.html',
        'modal_size': 'modal-lg',
        'form': TurnoForm()
    }
    return render(request, 'calendario.html', context)


def add_appointment(request):
    form = TurnoForm(json.loads(request.body))
    if form.is_valid():
        appointments = form.save()
        response_data = {
            'success': True,
            'appointments': [{
                'start_time': a.inicio,
                'end_time': a.fin,
                'state': a.estado
            } for a in appointments]
        }
    else:
        response_data = {'success': False, 'errors': form.errors}
    return JsonResponse(response_data)


def feed(request):
    kw = {}
    if 'start' in request.GET:
        kw['inicio__gte'] = parse_datetime(request.GET['start'])
    if 'end' in request.GET:
        kw['fin__lte'] = parse_datetime(request.GET['end'])

    turnos = [{
        'id': t.id,
        'title': str(t),
        'start': t.inicio.isoformat(), 
        'end': t.fin.isoformat(),
    } for t in Turno.objects.filter(**kw)]

    return JsonResponse(turnos, safe=False)
