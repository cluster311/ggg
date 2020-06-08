from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory

from centros_de_salud.models import CentroDeSalud
from pacientes.models import Consulta, Paciente
from profesionales.tests import FullUsersMixin
from recupero.models import Factura, TipoDocumentoAnexo, TipoPrestacion
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
        self.paciente = Paciente.objects.create(apellidos='Garcia', nombres='Alberto', sexo='masculino',
                                       fecha_nacimiento='1980-04-29',
                                       tipo_documento='DNI', numero_documento='24987563', nacionalidad='argentina',
                                       vinculo='Padre', grupo_sanguineo="0-"
                                       )
        self.consulta = Consulta.objects.create(centro_de_salud=self.cs, paciente=self.paciente)
        self.fact = Factura.objects.get(consulta=self.consulta)
        self.tipo_documentacion = TipoDocumentoAnexo.objects.create(nombre="TEST")
        self.tipo_prestacion = TipoPrestacion.objects.create(nombre="TEST", tipo=100)


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

