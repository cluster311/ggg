from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.urls import reverse
from datetime import datetime


from centros_de_salud.models import CentroDeSalud, Especialidad
from pacientes.models import Consulta, Paciente, Empresa, EmpresaPaciente
from obras_sociales.models import ObraSocial, ObraSocialPaciente
from recupero.models import Factura, TipoDocumentoAnexo, TipoPrestacion, FacturaPrestacion

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
            tipo_documento='DNI', numero_documento='27546859'
            )
        self.especialidad = Especialidad.objects.create(nombre='Especialidad 1')
        self.consulta = Consulta.objects.create(centro_de_salud=self.cs, paciente=self.paciente)
        self.tipo_documentacion = TipoDocumentoAnexo.objects.create(nombre="TEST")
        self.tipo_prestacion = TipoPrestacion.objects.create(nombre="TEST", tipo=100)        

        # Crear relación ObraSocial <=> Paciente
        ObraSocialPaciente.objects.create(paciente=self.paciente, obra_social=self.obra_social)

        os_paciente = self.paciente.m2m_obras_sociales.first().obra_social

        self.fact = Factura.objects.create(
            consulta=self.consulta,
            profesional=self.profesional,
            especialidad=self.especialidad, 
            obra_social=os_paciente,
            fecha_atencion=timezone.now(),
            centro_de_salud=self.cs,
            paciente=self.paciente,
        )
        # Crear relaciones FK
        FacturaPrestacion.objects.create(factura=self.fact, tipo=self.tipo_prestacion)

        self.empresa = Empresa.objects.create(nombre='Telescopios Hubble', direccion='Av Astronómica s/n', cuit='31-91203043-8')
        
        EmpresaPaciente.objects.create(empresa=self.empresa, paciente=self.paciente)


    def tearDown(self):
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()
        self.cs.delete()
        self.consulta.delete()
        self.fact.delete()
        self.tipo_documentacion.delete()
        self.tipo_prestacion.delete()
        self.paciente.delete()
        self.empresa.delete()
        self.obra_social.delete()

    def test_errores_devueltos_Anexo2(self):
        '''
            Al intentar generar un Anexo2 erróneo el sistema 
            nos devuelve los errores explicados
        '''

        self.client.login(username='recupero', password='recupero')

        # Ir a la url que dispara la generación del Anexo2
        url = reverse('recupero.anexo2', kwargs={'factura_id': self.fact.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        templates = [template.name for template in response.templates]

        # Si hubo errores en el Anexo2 la respuesta contendrá un dict con errores
        # y se usará el template anexo_errors.html
        self.assertTrue('errors' in response.context)
        self.assertTrue('recupero/anexo_errors.html' in templates)
