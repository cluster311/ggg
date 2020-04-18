from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from profesionales.models import Profesional
from centros_de_salud.models import CentroDeSalud, Especialidad, Servicio, ProfesionalesEnServicio
from usuarios.models import UsuarioEnCentroDeSalud


def start_roles_and_permissions():
    """ crear los grupos/roles iniciales del sistema """
    group_city, created = Group.objects.get_or_create(name=settings.GRUPO_CIUDADANO)
    group_admin, created = Group.objects.get_or_create(name=settings.GRUPO_ADMIN)
    group_prof, created = Group.objects.get_or_create(name=settings.GRUPO_PROFESIONAL)
    group_data, created = Group.objects.get_or_create(name=settings.GRUPO_DATOS)
    group_super, created = Group.objects.get_or_create(name=settings.GRUPO_SUPER_ADMIN)
    group_recupero, created = Group.objects.get_or_create(name=settings.GRUPO_RECUPERO)

    """ asignar los permisos iniciales a los roles en el sistema """
    perm_schedule_turno = Permission.objects.get(codename='can_schedule_turno', content_type__app_label='calendario')
    perm_viewmy_turno = Permission.objects.get(codename='can_view_misturnos', content_type__app_label='calendario')
    perm_cancel_turno = Permission.objects.get(codename='can_cancel_turno', content_type__app_label='calendario')
    # Definir perm_gestionar_turno = Permission.objects.get(codename='can_gestionar_turnos', content_type__app_label='calendario')
    perm_add_turno = Permission.objects.get(codename='add_turno', content_type__app_label='calendario')
    perm_view_turno = Permission.objects.get(codename='view_turno', content_type__app_label='calendario')
    perm_change_turno = Permission.objects.get(codename='change_turno', content_type__app_label='calendario')

    group_admin.permissions.add(perm_add_turno, perm_change_turno, perm_schedule_turno, perm_view_turno, perm_cancel_turno)
    group_city.permissions.add(perm_viewmy_turno)

    perm_add_consulta = Permission.objects.get(codename='add_consulta', content_type__app_label='pacientes')
    perm_view_consulta = Permission.objects.get(codename='view_consulta', content_type__app_label='pacientes')

    group_prof.permissions.add(perm_view_consulta, perm_add_consulta)

    perm_add_prof = Permission.objects.get(codename='add_profesional', content_type__app_label='profesionales')
    perm_view_prof = Permission.objects.get(codename='view_profesional', content_type__app_label='profesionales')
    perm_chg_prof = Permission.objects.get(codename='change_profesional', content_type__app_label='profesionales')
    perm_tablero_prof = Permission.objects.get(codename='can_view_tablero', content_type__app_label='profesionales')
    
    group_admin.permissions.add(perm_view_prof)  # lo necesita para filtrar la lista de profesionales al crear los turnos. TODO limitarlo de alguna forma
    group_data.permissions.add(perm_tablero_prof)
    group_super.permissions.add(perm_view_prof, perm_chg_prof, perm_add_prof)
    
    perm_tablero_oss = Permission.objects.get(codename='can_view_tablero', content_type__app_label='obras_sociales')
    perm_view_oss = Permission.objects.get(codename='view_obrasocial', content_type__app_label='obras_sociales')
    perm_add_oss = Permission.objects.get(codename='add_obrasocial', content_type__app_label='obras_sociales')
    perm_chg_oss = Permission.objects.get(codename='change_obrasocial', content_type__app_label='obras_sociales')

    group_data.permissions.add(perm_tablero_oss)
    group_super.permissions.add(perm_view_oss, perm_add_oss, perm_chg_oss)
    
    perm_tablero_cds = Permission.objects.get(codename='can_view_tablero', content_type__app_label='centros_de_salud')
    perm_add_serv = Permission.objects.get(codename='add_servicio', content_type__app_label='centros_de_salud')
    perm_view_serv = Permission.objects.get(codename='view_servicio', content_type__app_label='centros_de_salud')
    perm_chg_serv = Permission.objects.get(codename='change_servicio', content_type__app_label='centros_de_salud')
    perm_add_esp = Permission.objects.get(codename='add_especialidad', content_type__app_label='centros_de_salud')
    perm_view_esp = Permission.objects.get(codename='view_especialidad', content_type__app_label='centros_de_salud')
    perm_chg_esp = Permission.objects.get(codename='change_especialidad', content_type__app_label='centros_de_salud')
    perm_add_cds = Permission.objects.get(codename='add_centrodesalud', content_type__app_label='centros_de_salud')
    perm_view_cds = Permission.objects.get(codename='view_centrodesalud', content_type__app_label='centros_de_salud')
    perm_chg_cds = Permission.objects.get(codename='change_centrodesalud', content_type__app_label='centros_de_salud')
    perm_add_pes = Permission.objects.get(codename='add_profesionalesenservicio', content_type__app_label='centros_de_salud')
    perm_view_pes = Permission.objects.get(codename='view_profesionalesenservicio', content_type__app_label='centros_de_salud')
    perm_chg_pes = Permission.objects.get(codename='change_profesionalesenservicio', content_type__app_label='centros_de_salud')

    group_data.permissions.add(perm_tablero_cds)
    group_super.permissions.add(perm_view_serv, perm_chg_serv, perm_view_esp, perm_chg_esp,
                                perm_view_cds, perm_chg_cds, perm_view_pes, perm_chg_pes,
                                perm_add_serv, perm_add_esp, perm_add_cds, perm_add_pes)

    perm_add_ma = Permission.objects.get(codename='add_medidaanexa', content_type__app_label='especialidades')
    perm_view_ma = Permission.objects.get(codename='view_medidaanexa', content_type__app_label='especialidades')
    perm_chg_ma = Permission.objects.get(codename='change_medidaanexa', content_type__app_label='especialidades')
    perm_add_maesp = Permission.objects.get(codename='add_medidasanexasespecialidad', content_type__app_label='especialidades')
    perm_view_maesp = Permission.objects.get(codename='view_medidasanexasespecialidad', content_type__app_label='especialidades')
    perm_chg_maesp = Permission.objects.get(codename='change_medidasanexasespecialidad', content_type__app_label='especialidades')

    group_super.permissions.add(perm_view_ma, perm_chg_ma, perm_view_maesp, perm_chg_maesp,
                                perm_add_ma, perm_add_maesp)

    perm_view_fact = Permission.objects.get(codename='view_factura', content_type__app_label='recupero')
    perm_chg_fact = Permission.objects.get(codename='change_factura', content_type__app_label='recupero')
    perm_add_tda = Permission.objects.get(codename='add_tipodocumentoanexo', content_type__app_label='recupero')
    perm_view_tda = Permission.objects.get(codename='view_tipodocumentoanexo', content_type__app_label='recupero')
    perm_chg_tda = Permission.objects.get(codename='change_tipodocumentoanexo', content_type__app_label='recupero')
    perm_add_tp = Permission.objects.get(codename='add_tipoprestacion', content_type__app_label='recupero')
    perm_view_tp = Permission.objects.get(codename='view_tipoprestacion', content_type__app_label='recupero')
    perm_chg_tp = Permission.objects.get(codename='change_tipoprestacion', content_type__app_label='recupero')

    group_recupero.permissions.add(perm_view_fact, perm_chg_fact, perm_view_tda,
                                    perm_chg_tda, perm_view_tp, perm_chg_tp,
                                    perm_add_tda, perm_add_tp)
    
    perm_view_uecds = Permission.objects.get(codename='view_usuarioencentrodesalud', content_type__app_label='usuarios')
    perm_add_uecds = Permission.objects.get(codename='add_usuarioencentrodesalud', content_type__app_label='usuarios')
    perm_chg_uecds = Permission.objects.get(codename='change_usuarioencentrodesalud', content_type__app_label='usuarios')
    
    group_super.permissions.add(perm_view_uecds, perm_add_uecds, perm_chg_uecds)


def create_test_data():
    """ Crear centros de salud con diferentes 
        especialidades y profesionales asignados cada una.
        Sumar ademas usuarios con permisos en esos centros
        """

    for x in range(1, 4):
        # crear centros de salud y especialidades
        cs, created = CentroDeSalud.objects.get_or_create(nombre=f"Centro de Salud {x}")
        es, created = Especialidad.objects.get_or_create(nombre=f"Especialidad {x}")
        # crear un servicio en ese centro de salud para esa especialidad
        se, created = Servicio.objects.get_or_create(centro=cs, especialidad=es)
        for y in 'ABCDE':
            pr, created = Profesional.objects.get_or_create(nombres=f"Profesional {x}{y}",
                                                            numero_documento=f"900000{x}{y}")
            ps, created = ProfesionalesEnServicio.objects.get_or_create(servicio=se, profesional=pr)

            # crear un usuario para cada uno de los profesionales
            group_prof = Group.objects.get(name=settings.GRUPO_PROFESIONAL)
            us = User.objects.filter(username=f"prof{x}{y}")
            if us.count() == 0:
                user_prof = User.objects.create_user(username=f"prof{x}{y}",
                                                    email=f"prof{x}{y}@test.com",
                                                    password=f"prof{x}{y}")
                pr.user = user_prof
            else:
                user_prof = us[0]
            user_prof.groups.add(group_prof)
    
        # agregar un usuario administrativo con permisos para este centro de salud
        group_admin = Group.objects.get(name=settings.GRUPO_ADMIN)
        user_name = f"administrativo{x}"
        us = User.objects.filter(username=user_name)
        if us.count() == 0:
            user_admin = User.objects.create_user(username=user_name,
                                                  email=f"admin{x}@test.com", 
                                                  password=user_name)
        else:
            user_admin = us[0]
        user_admin.groups.add(group_admin)
        UsuarioEnCentroDeSalud.objects.get_or_create(usuario=user_admin,
                                                     centro_de_salud=cs)