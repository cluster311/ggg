from django import forms
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from calendario.models import Turno
from calendario.forms import FeedForm


def index(request):
    context = {
        'modal_title': 'Agregar turno',
        'modal_close': 'Cancelar',
        'modal_body_include': 'calendario/add_appointment_form.html'
    }
    return render(request, 'calendario.html', context)


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
