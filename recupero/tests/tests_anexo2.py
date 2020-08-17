from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from datetime import datetime


from centros_de_salud.models import CentroDeSalud, Especialidad
from pacientes.models import Consulta, Paciente, Empresa, EmpresaPaciente
from obras_sociales.models import ObraSocial, ObraSocialPaciente
from recupero.models import Factura, TipoDocumentoAnexo, TipoPrestacion, FacturaPrestacion
from cie10_django.models import CIE10

from profesionales.tests import FullUsersMixin, Profesional
from anexo2.docs import Anexo2
from recupero.views_anexo2 import Anexo2View


class Anexo2Tests(TestCase, FullUsersMixin):

    def setUp(self):
        self.create_users_and_groups()
        self.client = Client()

        self.cs = CentroDeSalud.objects.create(nombre=f"CdSTEST")
        self.obra_social = ObraSocial.objects.create(nombre="TEST_Obra_social", codigo=1234)
        self.paciente = Paciente.objects.create(
            apellidos='Garcia', nombres='Alberto', sexo='masculino',
            tipo_documento='DNI', fecha_nacimiento=datetime(1980,4,29).date(),
            numero_documento='24987563', nacionalidad='argentina',
            vinculo='Padre', grupo_sanguineo="0-"
            )
        self.profesional = Profesional.objects.create(
            apellidos='Sanchez', nombres='Romina', sexo='femenino',
            tipo_documento='DNI', numero_documento='27546859',
            matricula_profesional="987654"
            )
        self.especialidad = Especialidad.objects.create(nombre='Especialidad 1')

        self.tipo_documentacion = TipoDocumentoAnexo.objects.create(nombre="TEST")
        self.tipo_prestacion = TipoPrestacion.objects.create(nombre="TEST", tipo=100)

        ### Códigos CIE10 ###
        self.codigo_cie_1 = CIE10.objects.create(code="TEST01", level=1)
        self.codigo_cie_2 = CIE10.objects.create(code="TEST02", level=2)
        self.codigo_cie_3 = CIE10.objects.create(code="TEST03", level=3)

        # Crear relación ObraSocial <=> Paciente
        ObraSocialPaciente.objects.create(
            paciente=self.paciente, obra_social=self.obra_social,
            numero_afiliado="123456789"
            )

        self.os_paciente = self.paciente.m2m_obras_sociales.first().obra_social

        self.empresa = Empresa.objects.create(nombre='Telescopios Hubble', direccion='Av Astronómica s/n', cuit='31-91203043-8')
        
        EmpresaPaciente.objects.create(
            empresa=self.empresa, paciente=self.paciente,
            ultimo_recibo_de_sueldo=timezone.now()
        )

        ### Factura completa ###
        self.consulta = Consulta.objects.create(centro_de_salud=self.cs, paciente=self.paciente)

        self.factura_completa = Factura.objects.create(
            consulta=self.consulta,
            profesional=self.profesional,
            especialidad=self.especialidad, 
            obra_social=self.os_paciente,
            fecha_atencion=timezone.now(),
            centro_de_salud=self.cs,
            paciente=self.paciente,
            codigo_cie_principal=self.codigo_cie_1,
        )

        # Agregar CIE secundarios a la factura
        self.factura_completa.codigos_cie_secundarios.add(
            self.codigo_cie_2, self.codigo_cie_3
        )

        # Crear relaciones FK
        FacturaPrestacion.objects.create(factura=self.factura_completa, tipo=self.tipo_prestacion)

        ### Factura y consulta sin Centro de Salud ###

        self.consulta2 = Consulta.objects.create(paciente=self.paciente)

        self.factura_sin_CS = Factura.objects.create(
            consulta=self.consulta2,
            profesional=self.profesional,
            obra_social=self.os_paciente,
            fecha_atencion=timezone.now(),
            paciente=self.paciente,
        )

        FacturaPrestacion.objects.create(factura=self.factura_sin_CS, tipo=self.tipo_prestacion)

        ### Factura sin Profesional ###

        self.consulta3 = Consulta.objects.create(centro_de_salud=self.cs, paciente=self.paciente)

        self.factura_sin_profesional = Factura.objects.create(
            consulta=self.consulta3,
            especialidad=self.especialidad, 
            obra_social=self.os_paciente,
            fecha_atencion=timezone.now(),
            centro_de_salud=self.cs,
            paciente=self.paciente,
        )
        # Crear relaciones FK
        FacturaPrestacion.objects.create(factura=self.factura_sin_profesional, tipo=self.tipo_prestacion)

    def tearDown(self):
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()
        self.cs.delete()
        self.consulta.delete()
        self.consulta2.delete()
        self.consulta3.delete()
        self.factura_completa.delete()
        self.factura_sin_CS.delete()
        self.factura_sin_profesional.delete()
        self.tipo_documentacion.delete()
        self.tipo_prestacion.delete()
        self.paciente.delete()
        self.empresa.delete()
        self.obra_social.delete()

    def test_errores_Anexo2_incompleto(self):
        '''
            Al intentar generar un Anexo2 a partir de una factura
            con datos incompletos, se captura este error 
            y se notifica al usuario para que lo complete
        '''

        print('=== Test Anexo2 incompleto captura errores ===')

        self.client.login(username='recupero', password='recupero')

        # De esta forma se pueden parametrizar los tests
        # de cada factura con su respectivo error
        facturas = [
            (self.factura_sin_CS, b'Debe asignar un centro de salud en la factura'),
            (self.factura_sin_profesional, b'Debe asignar un profesional en la factura'),
        ]

        for factura, error in facturas:
            with self.subTest(factura=factura):

                # Ir a la url que dispara la generación del Anexo2
                url = reverse('recupero.anexo2', kwargs={'factura_id': factura.id})

                response = self.client.get(url)

                # Verificar que existen errores en la respuesta HTML
                self.assertIn(error, response.content)

                # Si hubo errores en el Anexo2 se pasarán en el context
                # un dict 'anexo2' y otro 'datos' con los errores
                self.assertTrue('anexo2' in response.context)
                self.assertTrue('datos' in response.context)
                
                templates = [template.name for template in response.templates]

                # Se usará el template anexo_errors.html
                self.assertTrue('recupero/anexo_errors.html' in templates)

    def test_permisos_Anexo2(self):
        '''
            Corroborar que se les deniega el acceso a ver el Anexo2 
            a usuarios que no tengan el rol recupero
        '''

        print('=== Test permisos Anexo2 ===')

        self.factory = RequestFactory()
        
        # Se definen los kwargs porque tienen que ser pasados junto con la request en el assert
        # https://stackoverflow.com/questions/48580465/django-requestfactory-loses-url-kwargs
        kwargs={'factura_id': self.factura_completa.id}
        url = reverse('recupero.anexo2', kwargs=kwargs)
        request = self.factory.get(url)

        # Lista de usuarios a probar
        users = [self.user_admin, self.user_anon, self.user_city, self.user_prof]

        for user in users:
            with self.subTest(user=user):

                request.user = user
                with self.assertRaises(PermissionDenied):
                    Anexo2View.as_view()(request, **kwargs) # Acá se pasan los kwargs definidos más arriba
        
    def test_cambio_estado_factura_Anexo2(self):
        '''
            Chequear que las facturas cambian al estado esperado 
            en caso de que el Anexo2 se genere correctamente o devuelva errores
        '''

        print('=== Test Cambio de estado de factura ===')

        self.client.login(username='recupero', password='recupero')

        facturas = [
            (self.factura_completa, 500), # ACEPTADA
            (self.factura_sin_CS, 400), # RECHAZADA
            (self.factura_sin_profesional, 400)
        ]

        for factura, estado_esperado in facturas:
            with self.subTest(factura=factura):

                # Ir a la url que dispara la generación del Anexo2
                url = reverse('recupero.anexo2', kwargs={'factura_id': factura.id})
                response = self.client.get(url)
                
                # Hacer una nueva petición a la BD para tomar
                # el valor actualizado del estado de cada factura
                
                fact_actualizada = Factura.objects.get(id=factura.id)

                self.assertEqual(fact_actualizada.estado, estado_esperado)