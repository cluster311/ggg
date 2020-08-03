from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.utils import timezone

from centros_de_salud.models import CentroDeSalud, Especialidad
from pacientes.models import Consulta, Paciente, Empresa, EmpresaPaciente
from profesionales.tests import FullUsersMixin, Profesional
from obras_sociales.models import ObraSocial, ObraSocialPaciente
from recupero.models import Factura, TipoDocumentoAnexo, TipoPrestacion, FacturaPrestacion
from recupero.views import FacturaListView, FacturaCreateView, FacturaDetailView, FacturaUpdateView
from recupero.views_anexo2 import Anexo2View
from recupero.views_tipo_documento_anexo import TipoDocumentoAnexoListView, TipoDocumentoAnexoCreateView, \
    TipoDocumentoAnexoDetailView, TipoDocumentoAnexoUpdateView
from recupero.views_tipo_prestacion import TipoPrestacionListView, TipoPrestacionCreateView, TipoPrestacionDetailView, \
    TipoPrestacionUpdateView


class RecuperoTests(TestCase, FullUsersMixin):

    def setUp(self):
        self.create_users_and_groups()
        self.factory = RequestFactory()

        self.cs = CentroDeSalud.objects.create(nombre=f"CdSTEST")
        self.obra_social = ObraSocial.objects.create(nombre="TEST_Obra_social", codigo=1234)
        self.paciente = Paciente.objects.create(
            apellidos='Garcia', nombres='Alberto', sexo='masculino',
            fecha_nacimiento='1980-04-29', tipo_documento='DNI',
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

    def test_factura_list_view(self):
        request = self.factory.get('/facturacion/')
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            FacturaListView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            FacturaListView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            FacturaListView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            FacturaListView.as_view()(request)

        request.user = self.user_recupero
        response = FacturaListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_factura_create_view(self):
        request = self.factory.get('/crear-factura/')
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            FacturaCreateView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            FacturaCreateView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            FacturaCreateView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            FacturaCreateView.as_view()(request)
        request.user = self.user_recupero
        response = FacturaCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_factura_detail_view(self):
        request = self.factory.get('/detalle-factura/' + str(self.fact.id))
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            FacturaDetailView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            FacturaDetailView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            FacturaDetailView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            FacturaDetailView.as_view()(request)
        request.user = self.user_recupero
        response = FacturaDetailView.as_view()(request, pk=self.fact.id)
        self.assertEqual(response.status_code, 200)

    def test_factura_update_view(self):
        request = self.factory.get('/editar-factura/' + str(self.fact.id))
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            FacturaUpdateView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            FacturaUpdateView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            FacturaUpdateView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            FacturaUpdateView.as_view()(request)
        request.user = self.user_recupero
        response = FacturaUpdateView.as_view()(request, pk=self.fact.id)
        self.assertEqual(response.status_code, 200)

    def test_Anexo2_view(self):
        request = self.factory.get('/anexo-II/' + str(self.fact.id))

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            Anexo2View.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            Anexo2View.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            Anexo2View.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            Anexo2View.as_view()(request)

        request.user = self.user_recupero
        response = Anexo2View.as_view()(request, factura_id=self.fact.id)
        self.assertEqual(response.status_code, 200)

    def test_TipoDocumentoAnexo_list_view(self):
        request = self.factory.get('/anexo-II/' + str(self.fact.id))

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoListView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoListView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoListView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoListView.as_view()(request)

        request.user = self.user_recupero
        response = TipoDocumentoAnexoListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_TipoDocumentoAnexo_create_view(self):
        request = self.factory.get('/crear-tipo-de-documentacion.html')

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoCreateView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoCreateView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoCreateView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoCreateView.as_view()(request)

        request.user = self.user_recupero
        response = TipoDocumentoAnexoCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_TipoDocumentoAnexo_detail_view(self):
        request = self.factory.get('/detalle-tipo-de-documentacion/' + str(self.tipo_documentacion.id))

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoDetailView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoDetailView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoDetailView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoDetailView.as_view()(request)

        request.user = self.user_recupero
        response = TipoDocumentoAnexoDetailView.as_view()(request, pk=self.tipo_documentacion.id)
        self.assertEqual(response.status_code, 200)

    def test_TipoDocumentoAnexo_update_view(self):
        request = self.factory.get('/editar-tipo-de-documentacion/' + str(self.tipo_documentacion.id))

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoUpdateView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoUpdateView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoUpdateView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoDocumentoAnexoUpdateView.as_view()(request)

        request.user = self.user_recupero
        response = TipoDocumentoAnexoUpdateView.as_view()(request, pk=self.tipo_documentacion.id)
        self.assertEqual(response.status_code, 200)

    def test_TipoPrestacion_list_view(self):
        request = self.factory.get('/tipo-de-prestacion.html')

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoPrestacionListView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoPrestacionListView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoPrestacionListView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoPrestacionListView.as_view()(request)

        request.user = self.user_recupero
        response = TipoPrestacionListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_TipoPrestacion_create_view(self):
        request = self.factory.get('/crear-tipo-de-prestacion.html')

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoPrestacionCreateView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoPrestacionCreateView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoPrestacionCreateView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoPrestacionCreateView.as_view()(request)

        request.user = self.user_recupero
        response = TipoPrestacionCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_TipoPrestacion_detail_view(self):
        request = self.factory.get('/detalle-tipo-de-prestacion/')

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoPrestacionDetailView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoPrestacionDetailView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoPrestacionDetailView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoPrestacionDetailView.as_view()(request)

        request.user = self.user_recupero
        response = TipoPrestacionDetailView.as_view()(request, pk=self.tipo_prestacion.id)
        self.assertEqual(response.status_code, 200)

    def test_TipoPrestacion_update_view(self):
        request = self.factory.get('/editar-tipo-de-prestacion/')

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            TipoPrestacionUpdateView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            TipoPrestacionUpdateView.as_view()(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            TipoPrestacionUpdateView.as_view()(request)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            TipoPrestacionUpdateView.as_view()(request)

        request.user = self.user_recupero
        response = TipoPrestacionUpdateView.as_view()(request, pk=self.tipo_prestacion.id)
        self.assertEqual(response.status_code, 200)

    # def test_errores_creacion_Anexo2(self):
    #     # Generar un error en la generación del anexo 2 y 
    #     # lo que se ve es esta nueva vista con los errores explicados
    #     request = self.factory.get('/anexo-II/' + str(self.fact.id))

    #     request.user = self.user_recupero

    #     # Juntar los datos para el Anexo2
    #     data = self.fact.as_anexo2_json()
    #     anx = Anexo2(data=data)

    #     # Generar el Anexo2
    #     res = anx.get_html()
        
    #     response = Anexo2View.as_view()(
    #         request, factura_id=self.fact.id)

    #     self.assertEqual(response.status_code, 200)