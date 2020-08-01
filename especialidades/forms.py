from dal import autocomplete
from django import forms
from django.forms import inlineformset_factory

from pacientes.models import Consulta
from .models import (MedidaAnexa,
                     MedidasAnexasEspecialidad,
                     MedidaAnexaEnConsulta
                    )


class MedidaAnexaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = MedidaAnexa
        fields = ['nombre', 'observaciones_para_el_que_mide']


class MedidasAnexasEspecialidadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)    
    
    class Meta:
        model = MedidasAnexasEspecialidad
        fields = ['especialidad', 'medida', 'obligatorio', 'observaciones_para_el_que_mide']


class MedidaAnexaEnConsultaForm(forms.ModelForm):

    valor = forms.DecimalField(widget=forms.NumberInput(attrs={'step': 0.25}))
    medida = forms.ModelChoiceField(queryset=MedidaAnexa.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        medida = MedidaAnexa.objects.get(id=self.initial['medida'])
        self.fields['valor'].label = medida.nombre

    class Meta:
        model = MedidaAnexaEnConsulta
        fields = ['valor', 'medida']


MedidaAnexaEnConsultaFormset = inlineformset_factory(Consulta, MedidaAnexaEnConsulta, form=MedidaAnexaEnConsultaForm, extra=0, can_delete=False)
