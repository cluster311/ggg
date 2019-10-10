from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from .models import Turno
from django import forms


class FeedForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


def index(request):
    return render(request, 'calendario.html')


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
