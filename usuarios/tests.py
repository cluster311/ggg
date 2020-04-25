from django.contrib.auth.models import User
from django.test import Client, TestCase
from core.base_permission import start_roles_and_permissions, create_test_data
from centros_de_salud.models import CentroDeSalud


class FullUserMixin:
    def create_users_and_groups(self):
        # Crear roles y permisos
        start_roles_and_permissions()
        create_test_data()

class AdministrativosTest(TestCase, FullUserMixin):

    def setUp(self):
        
        self.client = Client()
        self.create_users_and_groups()
        self.user_admin_1 = User.objects.filter(username='administrativo1').get()
    
    def test_login_administrativo(self):

        # Request sin loguearse
        response = self.client.get('/turnos/')
        self.assertRedirects(response, '/accounts/login/?next=/turnos/') 

        # Login con user administrativo1
        self.client.login(username=self.user_admin_1, password=self.user_admin_1)

        response = self.client.get('/turnos/')
        self.assertEqual(response.status_code, 200)

    def test_centro_salud_permitido(self):
        ''' Usuario `administrativo1` solo puede ver el centro de salud que se le asignó '''

        self.client.login(username=self.user_admin_1, password=self.user_admin_1)

        response = self.client.get('/turnos/')
        
        # Sacar CS permitidos del context (list)
        CS_Permitidos = response.context['user__centros_de_salud_autorizados']
        
        self.assertTrue(len(CS_Permitidos) == 1)
        self.assertEqual('Centro de Salud 1', CS_Permitidos[0].nombre)