from django.db import models
from django.utils import timezone
from cie10_django.models import CIE10
from model_utils.models import TimeStampedModel
from core.signals import app_log


class TipoDocumentoAnexo(models.Model):
    """ Cada uno de los documentos que se pueden adjuntar a una prestación """
    nombre = models.CharField(max_length=30, help_text='Tipo de documento')

    """
    Posibles valores usados en Córdoba/Argentina
    (definir un espacio donde crearlos cuando el usuario sea de esta zona).
    Parece algo dinámico y cambiante según regulaciones, mejor es que esto no
    sea fijo por ahora.

     - comprobante_de_cobertura: Documento comprobante de que el paciente
                                 tiene cobertura social vigente
     - solicitud_medica: solicitud del médico para esta prestación
     - informe_de_resultados: resultados del estudio
     - denuncia_internacion: Documento que notifica que se comienza una
                             internacion
     - odontograma: Documento específico de tratamientos dentales
     - formulario_de_atencion: formulario de atención con diagnóstico y firma
                               del médico que traslada y el que recibe
     - registro_de_sesiones: registro de sesiones diarias con firma del
                             paciente
    """

    def __str__(self):
        return self.nombre


class TipoPrestacion(models.Model):
    """ Cada uno de los tipos de atencion.
        Basado en la pésima base de datos: Nomenclador para HPGD """
    nombre = models.CharField(max_length=30, help_text='Tipo de atención')
    codigo = models.CharField(max_length=30, 
                              null=True, blank=True,
                              help_text='Código del servicio (de nomenclador si corresponde)')
    
    arancel = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    descripcion = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    anio_update = models.PositiveIntegerField(default=2019, help_text='Si viene del nomenclador indicar de que versión es')
    TIPO_DESCONOCIDO = 0
    TIPO_CONSULTA = 100
    TIPO_PRACTICA = 200
    TIPO_INTERNACION = 300
    TIPO_LABORATORIO = 400
    # el Anexo II al parecer solo permite estos tipos reales de atención.
    # https://github.com/cluster311/Anexo2
    tipos = ((TIPO_DESCONOCIDO, 'Desconocido'),
             (TIPO_CONSULTA, 'Consulta'),
             (TIPO_PRACTICA, 'Práctica'),
             (TIPO_INTERNACION, 'Internación'),
             (TIPO_LABORATORIO, 'Laboratorio')
             )
    tipo = models.PositiveIntegerField(choices=tipos, default=TIPO_CONSULTA)

    # DOCUMENTOS que deben generarse segun la atencion
    documentos_requeridos = models.ManyToManyField(
        TipoDocumentoAnexo,
        blank=True,
        related_name='requerido_en_tipos'
    )
    documentos_sugeridos = models.ManyToManyField(
        TipoDocumentoAnexo,
        blank=True,
        related_name='sugerido_en_tipos'
    )

    def __str__(self):
        return self.nombre
    
    @classmethod
    def importar_desde_nomenclador(cls):
        """ Traer todos los elementos del nomenclador
            No usamos NomencladorHPGD porque la base del nomenclador es muy mala
            Tratamos aqui de crear una base nueva derivada de aquella pero que se pueda
            completar y mejorar.
            Como no hay clave única podrían duplicarse, 
            solo para su uso con bases limpias"""
        from nhpgd.nomenclador import Nomenclador
        n = Nomenclador()
        # actualziar a los últimos datos
        n.download_csv()
        for i, nom in n.tree.items():
            nombre = nom['descripcion'][:29]
            arancel = 0 if nom['arancel'] == '' else nom['arancel']
            cls.objects.create(tipo=cls.TIPO_DESCONOCIDO,
                               nombre=nombre,
                               codigo=nom['codigo'],
                               descripcion=nom['descripcion'],
                               observaciones=nom['observaciones'],
                               arancel=arancel
                               )


class Prestacion(TimeStampedModel):
    """ una prestacion que se le da a un paciente """
    consulta = models.ForeignKey('pacientes.Consulta', on_delete=models.CASCADE, related_name='prestaciones')
    tipo = models.ForeignKey(TipoPrestacion, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.medicamento


class DocumentoAnexo(TimeStampedModel):
    """ Cada uno de los documentos que se pueden adjuntar a una prestacion """
    prestacion = models.ForeignKey(Prestacion, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.ForeignKey(TipoDocumentoAnexo, on_delete=models.CASCADE)

    # TODO definir un destino seguro y privado!
    documento_adjunto = models.FileField(upload_to='documentos_anexos')

    def __str__(self):
        return f'DOC {self.tipo.nombre} {self.id}'


class Factura(TimeStampedModel):
    """ Cada una de las unidades a cobrar a una obra social o programa de salud.
        Se crea solo en los casos en los que esperamos recuperar
        De aquí salen los formularios Anexo 2 (y otros según tipo de
        prestación)
        Ver imagen:https://github.com/cluster311/Anexo2/blob/master/originales/Anexo-II-RESOLUCION-487-2002.gif  # noqa
        Ver imagen: https://user-images.githubusercontent.com/3237309/64081477-fc091780-ccd7-11e9-88aa-6e8bfb34f6c2.png  # noqa
        Referencia de atencion en Anexo II
        atencion = {
            'tipo': 'consulta',  # | practica | internacion
            'especialidad': 'Especialidad médica',
            # codigos del nomenclador
            'codigos_N_HPGD': ['AA01', 'AA02', 'AA06', 'AA07'],
            'fecha': {'dia': 3, 'mes': 9, 'anio': 2019},
            'diagnostico_ingreso_cie10': {
            'principal': 'W020',
            'otros': ['w021', 'A189']
            }
        }
        """
    #TODO ver una forma de seguir las fechas de cada cambio
    # quizas statusfield + monitorfield de model-utils
    # https://django-model-utils.readthedocs.io/en/latest/fields.html#monitorfield
    EST_NUEVO = 100
    EST_INICIADO = 200  # tomamos la decision de tratar de recuperlo
    EST_ENVIADO_A_OSS = 300  # se lo mandamos a la obra social
    EST_RECHAZADO = 400  # la oss nos mando a freir churros
    EST_ACEPTADO = 500  # la oss nos acepto la factura
    EST_PAGADO = 600  # la oss nos pagó

    estados = ((EST_NUEVO, 'Nueva factura'),
               (EST_INICIADO, 'Iniciado'),
               (EST_ENVIADO_A_OSS, 'Enviada'),
               (EST_RECHAZADO, 'Rechazada'),
               (EST_ACEPTADO, 'Aceptada'),
               (EST_ACEPTADO, 'Pagada')
               )
    estado = models.PositiveIntegerField(choices=estados, default=EST_NUEVO)
    prestacion = models.OneToOneField(Prestacion, on_delete=models.CASCADE)
    obra_social = models.ForeignKey(
        'obras_sociales.ObraSocial',
        on_delete=models.CASCADE,
        related_name='facturas',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'Factura {self.id}'
    
    def define_oss(self):
        # ver si el paciente tiene OSS o le corresponde algun progeama de salud
        #TODO self.obra_social = X
        return
    
    def change_status(self, new_status):
        data = {'old_status': self.estado, 'new_status': new_status}
        app_log.send(sender=self.__class__,
                     code='CHANGE_STATUS_FACTURA',
                     severity=3,
                     description=None,
                     data=data)
        self.estado = new_status
        self.save()
    
