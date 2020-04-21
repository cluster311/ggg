from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.exceptions import PermissionDenied
from django.urls import reverse

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

    def tearDown(self):
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()

    def test_redireccion_no_logeado(self):
        response = self.client.get('/turnos/feed')
        self.assertRedirects(response, '/accounts/login/?next=/turnos/feed')

        response = self.client.get('/turnos/')
        self.assertRedirects(response, '/accounts/login/?next=/turnos/')

        #response = self.client.get('/turnos/feed_availables')
        #self.assertRedirects(response, '/accounts/login/?next=/turnos/feed')

    def test_logged(self):
        self.client.login(username=self.user_admin, password=self.user_admin)
        response = self.client.get('/turnos/feed')
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.user_city, password=self.user_city)
        response = self.client.get('/turnos/feed')
        self.assertEqual(response.status_code, 302)



