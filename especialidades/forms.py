from dal import autocomplete
from django import forms
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

    valor = forms.DecimalField(initial=0.0,
                               widget=forms.NumberInput(attrs={'step': 0.25})) 
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)    
    
    class Meta:
        model = MedidaAnexaEnConsulta
        fields = ['valor']

