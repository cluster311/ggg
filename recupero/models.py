from django.db import models
from django.utils import timezone
from nhpgd_django.models import NomencladorHPGD
from cie10_django.models import CIE10


class Factura(models.Model):
    """ Cada una de las unidades a cobrar a una obra social o programa de salud 
        De aquí salen los formularios Anexo 2 (y otros según tipo de prestación)
        Ver imagen: https://github.com/cluster311/Anexo2/blob/master/originales/Anexo-II-RESOLUCION-487-2002.gif
        Ver imagen: https://user-images.githubusercontent.com/3237309/64081477-fc091780-ccd7-11e9-88aa-6e8bfb34f6c2.png
        Referencia de atencion en Anexo II
        atencion = {'tipo': 'consulta',  # | practica | internacion
                    'especialidad': 'Especialidad médica',
                    'codigos_N_HPGD': ['AA01', 'AA02', 'AA06', 'AA07'],  # codigos del nomenclador
                    'fecha': {'dia': 3, 'mes': 9, 'anio': 2019},
                    'diagnostico_ingreso_cie10': {'principal': 'W020', 'otros': ['w021', 'A189']}}
        """
    fecha = models.DateField(default=timezone.now)
    obra_social = models.ForeignKey('obras_sociales.ObraSocial', on_delete=models.CASCADE, related_name='facturas')
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

    def __str__(self):
        return f'Factura {self.id}'


class TipoDocumentoAnexo(models.Model):
    """ Cada uno de los documentos que se pueden adjuntar a una prestacion """
    nombre = models.CharField(max_length=30, help_text='Tipo de documento')

    """
    Posibles valores usados en Córdoba/Argentina
    (definir un espacio desde donde crearlos cuando el usuario sea de esta zona)
    Parece algo dinamíco y cambiante segun regulaciones, mejor es que esto no sea fijo por ahora

     - comprobante_de_cobertura: Documento comprobante de que el paciente tiene cobertura social vigente
     - solicitud_medica: solicitud del médico para esta prestación
     - informe_de_resultados: resultados del estudio
     - denuncia_internacion: Documento que notifica que se comienza una internacion
     - odontograma: Documento específico de tratamientos dentales
     - formulario_de_atencion: formulario de atención con diagnóstico y firma del médico que traslada y el que recibe
     - registro_de_sesiones: registro de sesiones diarias con firma del paciente
    """

    def __str__(self):
        return self.nombre


class DocumentoAnexo(models.Model):
    """ Cada uno de los documentos que se pueden adjuntar a una prestacion """
    tipo = models.ForeignKey(TipoDocumentoAnexo, on_delete=models.CASCADE)

    # TODO definir un destino seguro y privado!
    documento_adjunto = models.FileField(upload_to='documentos_anexos')

    def __str__(self):
        return f'DOC {self.tipo} {self.id}'


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
    documentos_requeridos = models.ManyToManyField(TipoDocumentoAnexo, blank=True, related_name='requerido_en_tipos')
    documentos_sugeridos = models.ManyToManyField(TipoDocumentoAnexo, blank=True, related_name='sugerido_en_tipos')
    
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
    
    documentos_adjuntados = models.ManyToManyField(DocumentoAnexo, blank=True)