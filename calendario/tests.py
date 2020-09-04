import json
from datetime import datetime, timezone

from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.encoding import force_str

from calendario.models import Turno
from pacientes.models import Paciente
from obras_sociales.models import ObraSocialPaciente, ObraSocial
from calendario.views import feed, index, add_appointment, copy_appointments, agendar, edit_turn, cancelar_turno, \
    crear_sobreturno, confirm_turn
from centros_de_salud.models import CentroDeSalud, Especialidad, Servicio, ProfesionalesEnServicio
from core.base_permission import start_roles_and_permissions, create_test_users
from profesionales.models import Profesional
from usuarios.models import UsuarioEnCentroDeSalud


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
        self.cs = CentroDeSalud.objects.create(nombre=f"CdSTEST")
        self.cs2 = CentroDeSalud.objects.create(nombre=f"CdSTEST2")
        self.es = Especialidad.objects.create(nombre=f"EspTEST")
        self.se = Servicio.objects.create(centro=self.cs, especialidad=self.es)
        self.se2 = Servicio.objects.create(centro=self.cs2, especialidad=self.es)
        self.pr = Profesional.objects.create(nombres=f"ProfTEST", numero_documento=f"900000TEST")
        self.ps = ProfesionalesEnServicio.objects.create(servicio=self.se, profesional=self.pr)
        self.ps2 = ProfesionalesEnServicio.objects.create(servicio=self.se2, profesional=self.pr)
        self.tr = Turno.objects.create(inicio=datetime.now(tz=timezone.utc), fin=datetime.now(tz=timezone.utc), servicio=self.se, profesional=self.pr)
        self.tr2 = Turno.objects.create(inicio=datetime.now(tz=timezone.utc), fin=datetime.now(tz=timezone.utc), servicio=self.se2, profesional=self.pr)
        self.ucds = UsuarioEnCentroDeSalud.objects.create(usuario=self.user_admin, centro_de_salud=self.cs)

        self.paciente = Paciente.objects.create(apellidos='Garcia', nombres='Alberto', numero_documento='24987563')
        self.obra_social = ObraSocial.objects.create(nombre="TEST_Obra_social", codigo=1234)
        
        # Crear relación ObraSocial <=> Paciente
        self.os_paciente = ObraSocialPaciente.objects.create(
            paciente=self.paciente, obra_social=self.obra_social,
            numero_afiliado="123456789", tipo_beneficiario="titular", parentesco="conyuge"
            )

    def tearDown(self):
        self.user_city.delete()
        self.user_admin.delete()
        self.user_prof.delete()
        self.group_city.delete()
        self.group_admin.delete()
        self.group_prof.delete()
        self.tr.delete()
        self.tr2.delete()
        self.ps.delete()
        self.ps2.delete()
        self.ucds.delete()
        self.pr.delete()
        self.se.delete()
        self.se2.delete()
        self.cs.delete()
        self.es.delete()
        self.cs2.delete()
        self.paciente.delete()
        self.obra_social.delete()
        self.os_paciente.delete()

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

    def test_edit_turn(self):
        form_json = {"id": str(self.tr.pk),
                "state": str(2)
            }
        f = str(form_json).replace("\'", "\"")
        request = self.factory.put('/turnos/edit_turn/'+str(self.tr.pk), f)
        request.user = self.user_admin
        response = edit_turn(request, pk=self.tr.pk)
        self.assertEqual(response.status_code, 200)

        #caso error permiso denegado
        form_json = {"id": str(self.tr2.pk),
                     "state": str(2)
                     }
        f = str(form_json).replace("\'", "\"")
        request = self.factory.put('/turnos/edit_turn/' + str(self.tr2.pk), f)
        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            edit_turn(request, pk=self.tr2.pk)

    def test_cancelar_turno(self):
        form_json = {"id": str(self.tr.pk),
                "state": str(2)
            }
        f = str(form_json).replace("\'", "\"")
        request = self.factory.put('/turnos/cancelar_turn/'+str(self.tr.pk), f)
        request.user = self.user_admin
        response = cancelar_turno(request, pk=self.tr.pk)
        self.assertEqual(response.status_code, 200)

        # caso error permiso denegado
        form_json = {"id": str(self.tr2.pk),
                     "state": str(2)
                     }
        f = str(form_json).replace("\'", "\"")
        request = self.factory.put('/turnos/cancelar_turn/' + str(self.tr2.pk), f)
        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            cancelar_turno(request, pk=self.tr2.pk)


    def test_crear_sobreturno(self):
        form_json = {"id": str(self.tr.pk),
                     "state": str(2)
                     }
        f = str(form_json).replace("\'", "\"")
        request = self.factory.post('/turnos/crear_sobreturno/' + str(self.tr.pk))
        request.user = self.user_admin
        response = crear_sobreturno(request, pk=self.tr.pk)
        self.assertEqual(response.status_code, 200)

        # caso error permiso denegado
        form_json = {"id": str(self.tr2.pk),
                     "state": str(2)
                     }
        f = str(form_json).replace("\'", "\"")
        request = self.factory.post('/turnos/crear_sobreturno/' + str(self.tr2.pk))
        request.user = self.user_admin
        with self.assertRaises(PermissionDenied):
            crear_sobreturno(request, pk=self.tr2.pk)

    def test_confirmar_turno(self):
        """
            Cuando se agenda un turno se crea una consulta 
            que debe tener asignada la Obra Social elegida
            por el paciente.
        """

        data = {
            "id": str(self.tr.pk),
            "paciente": str(self.paciente.numero_documento),
            "obra_social": str(self.obra_social.pk)
        }

        # Es necesario serializar antes de enviar
        form_data = json.dumps(data)
        
        url = reverse('calendario.confirm', kwargs={'pk': self.tr.pk})

        request = self.factory.put(url, form_data)
        request.user = self.user_admin

        response = confirm_turn(request, pk=self.tr.pk)

        # Decodificar de bytes a Json
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        
        # El turno se creó con exito
        self.assertEqual(response_data.get('success'), True)

        # El turno se confirmó
        self.assertEqual(
            response_data.get('turno').get('estado'), 
            'Asignado'
        )

        # El turno tiene asignado el paciente que se envió en el formulario
        self.assertEqual(
            response_data.get('turno').get('paciente'), 
            str(self.paciente)
        )
        
        # La consulta creada tiene la OS con la que se agendó el turno
        self.assertEqual(
            self.tr.consulta.obra_social_id, 
            self.obra_social.pk
        )