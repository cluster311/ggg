from django.contrib.auth.models import User
from django.test import TestCase
from pacientes.models import Paciente
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


class TestCore(TestCase):

    def test_paciente_from_sisa(self):
        # requiere credenciales en local_settings cargadas para SISA
        # requiere un mock
        p = Paciente(nombres="Andres", apellidos="Vazquez", numero_documento="26453653")
        p.save()

        assert p.nombres == "Andres"

        """
        ok, msg = p.get_obras_sociales_from_sisa()
        if ok:  # es posible que no se tengan las credenciales
            assert ok is True
            assert msg is None
            assert p.obras_sociales.count() == 1
            assert p.obras_sociales.all()[0].codigo == "904001"
            assert p.obras_sociales.all()[0] == "O.S.P. CORDOBA (APROSS)"

            # la segunda vez
            ok, msg = p.get_obras_sociales_from_sisa()
            assert ok is True
            assert msg.startswith('Cache valido aún')

            p.obras_social_updated = timezone.now() - timedelta(
                seconds=settings.CACHED_OSS_INFO_SISA_SECONDS + 100
            )

            ok, msg = p.get_obra_social()
            assert ok == True
            assert msg is None
        """


class UsuarioTest(TestCase):
    def tearDown(self):
        self.user.delete()

    def test_nuevo_usuario(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.user = user
        self.assertEqual(user.groups.count(), 0)

