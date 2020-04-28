import json


from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from calendario.views import feed, index, add_appointment, copy_appointments, agendar
from core.base_permission import start_roles_and_permissions, create_test_users


class FullUsersMixin:
    def create_users_and_groups(self):
        #create permissions group
        start_roles_and_permissions()
        ret = create_test_users()

        self.group_city = ret['group_city']
        self.group_admin = ret['group_admin']
        self.group_prof = ret['group_prof']
        self.group_recupero = ret['group_recupero']

        self.user_anon = ret['user_anon']
        self.user_city = ret['user_city']
        self.user_admin = ret['user_admin']
        self.user_prof = ret['user_prof']
        self.user_recupero = ret['user_recupero']


class CalendarioTests(TestCase, FullUsersMixin):

    def setUp(self):
        self.c = Client()
        self.create_users_and_groups()
        self.factory = RequestFactory()

    def tearDown(self):
        #self.user_anon.delete()
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()

    def test_redireccion_no_logeado(self):
        request = self.factory.get('/turnos/feed')
        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            feed(request)

        request = self.factory.get('/turnos/')
        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            index(request)

        request = self.factory.get('/turnos/appointments/')
        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            add_appointment(request)

        request = self.factory.get('/turnos/appointments/copy/')
        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            copy_appointments(request)

        request = self.factory.get('/turnos/agendar/')
        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            agendar(request)

    def test_loggeado_feed(self):
        request = self.factory.get('/turnos/feed')
        request.user = self.user_admin
        response = feed(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            feed(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            feed(request)

        request.user = self.user_recupero
        with self.assertRaises(PermissionDenied):
            feed(request)

    def test_loggeado_index(self):
        request = self.factory.get('/turnos/')
        request.user = self.user_admin
        response = index(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            index(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            index(request)

        request.user = self.user_recupero
        with self.assertRaises(PermissionDenied):
            index(request)

    def test_loggeado_add_appointment(self):
        #responde 405 porque faltan enviar formulario y datos que recibe en formato json
        request = self.factory.post('/turnos/appointments/')
        #request.user = self.user_admin
        #response = add_appointment(request)
        #self.assertEqual(response.status_code, 405)

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            add_appointment(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            add_appointment(request)

        request.user = self.user_recupero
        with self.assertRaises(PermissionDenied):
            add_appointment(request)

    def test_loggeado_add_appointment_copy(self):
        # falta agregar parametros de fecha pero copiaria turnos
        request = self.factory.get('/turnos/appointments/copy/')
        #request.user = self.user_admin
        #response = copy_appointments(request)
        #self.assertEqual(response.status_code, 405)

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            copy_appointments(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            copy_appointments(request)

        request.user = self.user_recupero
        with self.assertRaises(PermissionDenied):
            copy_appointments(request)

    def test_loggeado_agendar(self):
        request = self.factory.post('/turnos/agendar/')
        #request.user = self.user_admin
        #response = add_appointment(request)
        #self.assertEqual(response.status_code, 200)

        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            agendar(request)

        request.user = self.user_prof
        with self.assertRaises(PermissionDenied):
            agendar(request)

        request.user = self.user_recupero
        with self.assertRaises(PermissionDenied):
            agendar(request)

