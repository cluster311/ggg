from django.db import models
from core.models import Persona
from address.models import AddressField
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from core.models import DatoDeContacto


class Profesional(Persona):
    matricula_profesional = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    profesion = models.CharField(max_length=190, null=True, blank=True)
    direccion = AddressField(null=True, blank=True, on_delete=models.SET_NULL)
    datos_de_contacto = GenericRelation(
        'core.DatoDeContacto',
        related_query_name='profesionales',
        null=True,
        blank=True
    )

    def __str__(self):
        apellidos = "" if self.apellidos is None else self.apellidos
        return f"{self.nombres} {apellidos}"

    def agregar_dato_de_contacto(self, tipo, valor):
        type_ = ContentType.objects.get_for_model(self)
        try:
            DatoDeContacto.objects.get(
                content_type__pk=type_.id,
                object_id=self.id,
                tipo=tipo,
                valor=valor
            )
        except DatoDeContacto.DoesNotExist:
            DatoDeContacto.objects.create(
                content_object=self,
                tipo=tipo,
                valor=valor
            )

    def importar_matriculado(self, row):
        """Importar desde una base de datos específica matriculados.
        Ejemplo de row de Excel
            AFILIADO: 42000
            NOMBRE: JUAN PEREZ
            PROFESION: LIC. EN PSICOLOGIA
            DOCUMENTO: 5556460
            TELEFONO: 03555-555555
            DOMICILIO: CHACO 31
            BARRIO
            LOCALIDAD: RIO CEBALLOS
            DEPARTAMENTO: COLON
            VOTA: S
        """
        self.nombres = row["NOMBRE"].strip()
        self.matricula_profesional = str(row["AFILIADO"])
        self.profesion = row["PROFESION"].strip()
        self.numero_documento = str(row["DOCUMENTO"])
        tel = row.get("TELEFONO", "")
        tel = str(tel) if type(tel) == int else tel.strip()
        # self.localidad = row.get('LOCALIDAD', '').strip()
        # self.departamento = row.get('DEPARTAMENTO', '').strip()
        # domicilio = '{}, {}, {}, {}, Córdoba'.format(
        #   row.get('DOMICILIO', '').strip(),
        #   row.get('BARRIO', ''),
        #   self.localidad,
        #   self.departamento
        # )
        # self.domicilio = domicilio
        self.agregar_dato_de_contacto('teléfono', tel)

    class Meta:
        permissions = [
            (
                "can_view_tablero",
                "Puede ver los tableros de comandos sobre profesionales",
            )
        ]
        verbose_name_plural = "Profesionales"
