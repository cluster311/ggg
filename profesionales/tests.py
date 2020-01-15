from django.contrib.auth.models import User, Permission, Group
from django.test import TestCase, RequestFactory
from django.test import Client
from django.conf import settings

from .views import ProfesionalHome


class ProfesionalesTests(TestCase):
    
    def setUp(self):
        #create permissions group
        self.group_city, created = Group.objects.get_or_create(name=settings.GRUPO_CIUDADANO)
        self.group_admin, created = Group.objects.get_or_create(name=settings.GRUPO_ADMIN)
        self.group_prof, created = Group.objects.get_or_create(name=settings.GRUPO_PROFESIONAL)
        
        self.c = Client()
        self.user_city = User.objects.create_user(username="city", email="city@test.com", password="city")
        self.user_admin = User.objects.create_user(username="admin", email="admin@test.com", password="admin")
        self.user_prof = User.objects.create_user(username="prof", email="prof@test.com", password="prof")

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
    class ProfesionalHomeTest(TestCase):
        def test_environment_set_in_context(self):
            request = RequestFactory().get('/')
            view = ProfesionalHome()
            view.setup(request)

            context = view.get_context_data()
            self.assertIn('hoy', context)
            self.assertIn('estados', context)
    