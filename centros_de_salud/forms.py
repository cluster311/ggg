from dal import autocomplete
from django import forms
from django.contrib.gis import forms as gisforms
from .models import ProfesionalesEnServicio, Servicio
from profesionales.models import Profesional
from centros_de_salud.models import CentroDeSalud


class ProfesionalesEnServicioForm(forms.ModelForm):

    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profesional-autocomplete",
            attrs={"data-placeholder": "Ingrese nombre o dni del profesional"}
        ),
    )

    servicio = forms.ModelChoiceField(
        label='Servicio',
        queryset=Servicio.objects.all()
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user is not None:
            csp = user.centros_de_salud_permitidos.all()
            centros_de_salud_permitidos = [c.centro_de_salud for c in csp]
            qs = Servicio.objects.filter(centro__in=centros_de_salud_permitidos)
            self.fields['servicio'].queryset = qs

    class Meta:
        model = ProfesionalesEnServicio
        fields = ['servicio', 'profesional', 'estado']


class ServicioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user is not None:
            csp = user.centros_de_salud_permitidos.all()
            permitidos = [c.centro_de_salud.id for c in csp]
            self.fields['centro'].queryset = CentroDeSalud.objects.filter(pk__in=permitidos)

    class Meta:
        model = Servicio
        fields = ['centro', 'especialidad']


class CentroDeSaludForm(gisforms.ModelForm):
    ubicacion = gisforms.PointField(
        widget=gisforms.OSMWidget(
            attrs={'map_width': 600,
                   'map_height': 400,
                   'template_name': 'gis/openlayers-osm.html',
                   'default_lat':-34.6037673975556,
                   'default_lon':-58.38164806365966,
                   'default_zoom': 12}))
    class Meta:
        model = CentroDeSalud
        fields = '__all__'