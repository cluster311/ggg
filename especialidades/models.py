from django.db import models
# TODO mover la clase centros_de_salud.Especialidad aquí


class MedidaAnexa(models.Model):
    """ Cada vez que se hace alguna consulta médica vinculada
        a un especialidad hay requisitos que se piden.
        Por ejemplo medir masa corporal, peso y tension arterial.
        Por ahora solo numéricas pero esto podrían ser objetos más complejos
    """
    nombre = models.CharField(max_length=120)
    observaciones_para_el_que_mide = models.TextField(null=True, 
                                                      blank=True,
                                                      help_text='Texto que verá el profesional que mide')
    
    def __str__(self):
        return self.nombre


class MedidasAnexasEspecialidad(models.Model):
    """ Cada vez que se hace alguna consulta médica vinculada
        a un especialidad hay requisitos que se piden.
        Por ejemplo medir masa corporal, peso, tension arterial.
    """
    especialidad = models.ForeignKey('centros_de_salud.Especialidad',
                                     on_delete=models.CASCADE,
                                     related_name='medidas_anexas'
                                    )
    medida = models.ForeignKey(MedidaAnexa, on_delete=models.CASCADE,
                               related_name='especialidades')
    obligatorio = models.BooleanField(default=True)
    observaciones_para_el_que_mide = models.TextField(null=True, 
                                                      blank=True,
                                                      help_text='Texto que verá el profesional que mide en esta especialidad')

    def __str__(self):
        return f'{self.medida} en {self.especialidad}'
    
    class Meta:
        unique_together = [['especialidad', 'medida']]


class MedidaAnexaEnConsulta(models.Model):
    consulta = models.ForeignKey('pacientes.Consulta', on_delete=models.CASCADE,
                                 related_name='medidas_anexas')
    medida = models.ForeignKey(MedidaAnexa,
                               on_delete=models.CASCADE,
                               related_name='mediciones')
    # mientras no definamos objetos con formatos especificos
    # solo iremos con numeros de amplio rango
    valor = models.DecimalField(max_digits=13, decimal_places=2, default=0.0)
