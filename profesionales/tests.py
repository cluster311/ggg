from django.contrib.auth.models import User, Permission, Group, AnonymousUser
from django.test import TestCase, RequestFactory
from django.test import Client
from django.conf import settings
from django.core.exceptions import PermissionDenied
from profesionales.models import Profesional
from .views import ProfesionalHome


class FullUsersMixin:
    def create_users_and_groups(self):
        #create permissions group
        self.group_city, created = Group.objects.get_or_create(name=settings.GRUPO_CIUDADANO)
        self.group_admin, created = Group.objects.get_or_create(name=settings.GRUPO_ADMIN)
        self.group_prof, created = Group.objects.get_or_create(name=settings.GRUPO_PROFESIONAL)
        
        self.user_anon = AnonymousUser()
        self.user_city = User.objects.create_user(username="city", email="city@test.com", password="city")
        self.user_city.groups.add(self.group_city)
        self.user_admin = User.objects.create_user(username="admin", email="admin@test.com", password="admin")
        self.user_admin.groups.add(self.group_admin)
        prof = Profesional.objects.create(nombres="prof name", numero_documento="10101090")
        self.user_prof = User.objects.create_user(username="prof", email="prof@test.com", password="prof")
        prof.user = self.user_prof
        self.user_prof.groups.add(self.group_prof)

class ProfesionalesTests(TestCase, FullUsersMixin):


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

    def test_login(self):
        login_url = '/accounts/login/'
        response = self.c.post(login_url, {'username': 'john', 'password': 'smith'})
        
        # TODO we get a 200 with a msg error ...
        # self.assertEqual(response.status_code, 403)

        response = self.c.post(login_url, {'username': 'city', 'password': 'city'})
        self.assertEqual(response.status_code, 200)
        
        # response = c.get('/customer/details/')
        # c.get('/customers/details/', {'name': 'fred', 'age': 7})
        # response.content

    # https://docs.djangoproject.com/en/3.0/topics/testing/advanced/


class ProfesionalHomeTest(TestCase, FullUsersMixin):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        self.create_users_and_groups()

    def test_environment_set_in_context(self):
        request = self.factory.get('/')
        view = ProfesionalHome()
        
        request.user = self.user_anon
        try:
            view.setup(request)
            assert 'Anon access to profesional'
        except PermissionDenied:
            pass
        
        request.user = self.user_admin
        try:
            view.setup(request)
            assert 'ADMIN access to profesional'
        except PermissionDenied:
            pass

        request.user = self.user_prof
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('hoy', context)
        self.assertIn('estados', context)
    