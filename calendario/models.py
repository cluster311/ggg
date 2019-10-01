from django.db import models


class Turno(models.Model):    
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    servicio = models.ForeignKey('centros_de_salud.Servicio', on_delete=models.CASCADE)
    profesional = models.ForeignKey('profesionales.Profesional',  blank=True, null=True, on_delete=models.SET_NULL)
    paciente = models.ForeignKey('pacientes.Paciente', blank=True, null=True, on_delete=models.SET_NULL)



    def __str__(self):
        return f'{self.servicio.especialidad} '
