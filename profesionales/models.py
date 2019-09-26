from django.db import models


class Profesional(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)

    dni = models.CharField(max_length=20, null=True, blank=True)
    matricula_profesional = models.CharField(max_length=20, null=True, blank=True)

    # TODO: importar datos desde el sistema municipal

    def __str__(self):
        apellidos = '' if self.apellidos is None else self.apellidos
        return f'{self.nombres, apellidos}'

    class Meta:
        permissions = [
            ('can_view_tablero', 'Puede ver los tableros de comandos sobre profesionales'),
            ]
