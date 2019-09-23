from django.db import models
from core.models import Persona


class Profesional(Persona):
    matricula_profesional = models.CharField(max_length=20, null=True, blank=True)

    # TODO: importar datos desde el sistema municipal

    def __str__(self):
        return f'{self.nombres, self.apellidos}'

    class Meta:
        verbose_name_plural = 'Profesionales'
