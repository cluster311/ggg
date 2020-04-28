from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.core.exceptions import PermissionDenied
from core.base_permission import start_roles_and_permissions, create_test_data
from centros_de_salud.models import CentroDeSalud
from calendario.forms import TurnoForm
from centros_de_salud.models import Servicio

class FullUserMixin:
    def create_users_and_groups(self):
        # Crear roles y permisos
        start_roles_and_permissions()
        create_test_data()

class AdministrativosTest(TestCase, FullUserMixin):
    ''' Tests de usuario administrativo en operaciones con turnos,
        CS autorizados, servicios y profesionales '''

    def setUp(self):
        
        self.client = Client()
        self.create_users_and_groups()
        self.user_admin_1 = User.objects.filter(username='administrativo1').get()
    
    def test_login_administrativo(self):

        # Request sin loguearse
        with self.assertRaises(PermissionDenied):
            response = self.client.get('/turnos/')

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
    
    def test_especialidades_permitidas_form_turno(self):
        ''' Usuario `administrativo1` solamente puede agregar turnos de 
            Especialidades en Centros de Salud permitidos '''

        self.client.login(username=self.user_admin_1, password=self.user_admin_1)

        # Instanciar el formulario de Turnos para nuestro usuario
        form = TurnoForm(user=self.user_admin_1)

        # Obtener la especialidad (Servicio de un centro de salud) 
        # permitida para este usuario
        
        # El método get() devuelve un error si existe más de 1 objeto
        servicio = form.fields['servicio'].queryset.get()

        # El usuario administrativo1 solo puede agendar turnos
        # de especialidades del CS 1 que es el que tiene asignado
        self.assertEqual(servicio.centro.nombre, 'Centro de Salud 1')
        self.assertEqual(servicio.especialidad.nombre, 'Especialidad 1')

    def test_profesionales_corresponden_especialidad(self):
        ''' Profesionales listados en el formulario de turno
            deberían ser solamente los que corresponen al 
            servicio elegido '''
        
        self.client.login(username=self.user_admin_1, password=self.user_admin_1)

        servicio1 = Servicio.objects.filter(centro__nombre='Centro de Salud 1').get()

        # Url que devuelve los profesionales en base al servicio colocado en el form
        url = f'/core/profesional-autocomplete-por-servicio/{servicio1.id}'

        response = self.client.get(url)

        # Sacar los profesionales de la response
        profesionales = response.json().get('results')

        # Guardo el nombre de cada profesional en un array
        nombres_profs = [] 
        for prof in profesionales:
            nombres_profs.append(prof['text'])
        
        valor_esperado = ['Profesional 1A ', 'Profesional 1B ', 'Profesional 1C ', 'Profesional 1D ', 'Profesional 1E ']

        self.assertEqual(nombres_profs, valor_esperado)
