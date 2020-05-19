from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.exceptions import PermissionDenied
from core.base_permission import start_roles_and_permissions, create_test_users, create_test_paciente_data
from .models import Paciente, Consulta
from .views import ConsultaListView, ConsultaDetailView


class FullUsersMixin:
    def create_users_and_groups(self):
        # create permissions group
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


class PacienteTests(TestCase, FullUsersMixin):

    def setUp(self):
        self.c = Client()
        self.create_users_and_groups()
        paciente = Paciente.objects.create(apellidos='Garcia', nombres='Alberto', sexo='masculino',
                                       fecha_nacimiento='1980-04-29',
                                       tipo_documento='DNI', numero_documento='24987563', nacionalidad='argentina',
                                       vinculo='Padre', grupo_sanguineo="0-"
                                       )
        consulta = Consulta()
        consulta.paciente = paciente
        consulta.save()
        self.factory = RequestFactory()

    def tearDown(self):
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()
        p = Paciente.objects.get(apellidos='Garcia', nombres='Alberto', sexo='masculino',
                                       fecha_nacimiento='1980-04-29',
                                       tipo_documento='DNI', numero_documento='24987563', nacionalidad='argentina',
                                       vinculo='Padre', grupo_sanguineo="0-"
                                 )
        consulta = Consulta.objects.get(paciente=p)
        consulta.delete()
        p.delete()


    def test_consulta_list_view(self):
        request = self.factory.get('/pacientes/24987563/historia/')
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            ConsultaListView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            ConsultaListView.as_view()(request)

        request.user = self.user_prof
        response = ConsultaListView.as_view()(request, dni=24987563)
        self.assertEqual(response.status_code, 200)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            ConsultaListView.as_view()(request)

    def test_consulta_detail_view(self):
        request = self.factory.get('/pacientes/24987563/historia/1')
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            ConsultaDetailView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            ConsultaDetailView.as_view()(request)

        request.user = self.user_prof
        paciente = Paciente.objects.get(numero_documento=24987563)
        consulta = Consulta.objects.filter(paciente=paciente)[0]
        response = ConsultaDetailView.as_view()(request, dni=24987563, pk=consulta.pk)
        self.assertEqual(response.status_code, 200)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            ConsultaDetailView.as_view()(request)

    def test_evolucion_update_view(self):
        request = self.factory.get('/pacientes/24987563/historia/')
        request.user = self.user_city
        with self.assertRaises(PermissionDenied):
            ConsultaListView.as_view()(request)

        request.user = self.user_anon
        with self.assertRaises(PermissionDenied):
            ConsultaListView.as_view()(request)

        request.user = self.user_prof
        paciente = Paciente.objects.get(numero_documento=24987563)
        response = ConsultaListView.as_view()(request, dni=24987563, id=paciente.id)
        self.assertEqual(response.status_code, 200)

        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            ConsultaListView.as_view()(request)
