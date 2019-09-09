from django.db import models


class Profesional(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    
    dni = models.CharField(max_length=20, null=True, blank=True)
    matricula_profesional = models.CharField(max_length=20, null=True, blank=True)
    
    # TODO: importar datos desde el sistema municipal
    
    def __str__(self):
        return f'{self.nombres, self.apellidos}'
