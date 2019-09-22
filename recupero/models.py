from django.db import models
from django.utils import timezone
from nhpgd_django.models import NomencladorHPGD
from cie10_django.models import CIE10


class Factura(models.Model):
    """ Cada una de las unidades a cobrar a una obra social o programa de salud 
        De aquí salen los formularios Anexo 2 (y otros según tipo de prestación)
        Ver la imagen: https://github.com/cluster311/Anexo2/blob/master/originales/Anexo-II-RESOLUCION-487-2002.gif
        Referencia de atencion en Anexo II
        atencion = {'tipo': 'consulta',  # | practica | internacion
                    'especialidad': 'Especialidad médica',
                    'codigos_N_HPGD': ['AA01', 'AA02', 'AA06', 'AA07'],  # codigos del nomenclador
                    'fecha': {'dia': 3, 'mes': 9, 'anio': 2019},
                    'diagnostico_ingreso_cie10': {'principal': 'W020', 'otros': ['w021', 'A189']}}
        """
    fecha = models.DateField(default=timezone.now)
    obra_social = models.ForeignKey('core.ObraSocial', on_delete=models.CASCADE, related_name='facturas')
    centro_de_salud = models.ForeignKey('centros_de_salud.CentroDeSalud',
                                        on_delete=models.CASCADE, related_name='facturas')
    profesional = models.ForeignKey('profesionales.Profesional', null=True, blank=True,
                                    on_delete=models.CASCADE, related_name='facturas')
    # ver si esta lista podría ser una columna mas en el nomenclador o de donde vienen los datos válidos
    # Odontología es un ejemplo válido de especialidad pero no hay mayores especificaciones
    especialidad = models.CharField(max_length=50)
    codigo_cie_principal = models.ForeignKey(CIE10, on_delete=models.SET_NULL,
                                             null=True, blank=True,
                                             related_name='facturas')
    cies_extras = models.ManyToManyField(CIE10, blank=True, related_name='extras_facturas')


class TipoPrestacion(models.Model):
    """ Cada uno de los tipos de atencion """
    nombre = models.CharField(max_length=30, help_text='Tipo de atención')
    # Ejemplos
    # Enfermería, Imagenes - Rayos X, Imagenes - Ecografía, Imagenes - Mamografía, Imagenes - Otros
    # Internacion breve, Internacion prolongada, Atencion de urgencias, emergencias y traslados
    # Odontología, Kinesiología
    
    TIPO_CONSULTA = 100
    TIPO_PRACTICA = 200
    TIPO_INTERNACION = 300
    # el Anexo II al parecer solo permite estos tipos reales de atención.
    # https://github.com/cluster311/Anexo2
    tipos = ((TIPO_CONSULTA, 'Consulta'),
             (TIPO_PRACTICA, 'Práctica'),
             (TIPO_INTERNACION, 'Internación')
             )
    tipo = models.PositiveIntegerField(choices=tipos, default=TIPO_CONSULTA)

    # DOCUMENTOS que deben generarse segun la atencion
    requiere_anexo_ii = models.BooleanField(default=True, help_text='Requiere Anexo II')
    requiere_comprobante_de_cobertura = models.BooleanField(default=True, help_text='Requiere anexar documento de comprobante a pertura')
    requiere_solicitud_medica = models.BooleanField(default=False, help_text='Requiere original o copia de la solicitud del médico')
    requiere_informe_de_resultados = models.BooleanField(default=False, help_text='Requiere Informe de resultados del estudio')
    requiere_denuncia_internacion = models.BooleanField(default=False, help_text='Requiere Anexo A: Denuncia de internación')
    requiere_odontograma = models.BooleanField(default=False, help_text='Requiere Odontograma')
    requiere_formulario_de_atencion = models.BooleanField(default=False, help_text='Requiere formulario de atención con diagnóstico y firma del médico que traslada y el que recibe.')
    requiere_registro_de_sesiones = models.BooleanField(default=False, help_text='Requiere registro de sesiones diarias con firma del paciente')

    def __str__(self):
        return self.nombre


class Prestacion(models.Model):
    """ Cada una de las atenciones a un paciente/beneficiario 
        cubiertos por algun programa, obra social o prepaga 
        """
    fecha = models.DateField(default=timezone.now, help_text='Fecha de la prestación')
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='prestaciones')
    tipo = models.ForeignKey(TipoPrestacion, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    nomenclador = models.ForeignKey(NomencladorHPGD,
                                    on_delete=models.CASCADE,
                                    related_name='prestaciones',
                                    help_text='Servicio realizado o entregado')
    
