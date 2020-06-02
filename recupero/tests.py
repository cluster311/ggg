from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from profesionales.tests import FullUsersMixin
from recupero.models import Factura
from recupero.views import FacturaListView, FacturaCreateView, FacturaDetailView, FacturaUpdateView
from recupero.views_anexo2 import Anexo2View


class RecuperoTests(TestCase, FullUsersMixin):

    def setUp(self):
        self.create_users_and_groups()
        self.factory = RequestFactory()
        self.fact = Factura.objects.create(estado=100)

    def tearDown(self):
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()
        self.fact.delete()

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

'''
    def test_Anexo2View_view(self):
        request = self.factory.get('/anexo-II/' + str(self.fact.id))

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            Anexo2View.as_view()(request, factura_id=self.fact.id)

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
'''

