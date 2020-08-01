# !/usr/bin/python

import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User, Group, Permission

from core.base_permission import start_roles_and_permissions


class Command(BaseCommand):
    help = """Crear los grupos y permisos iniciales"""

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Nombre del usuario')
        parser.add_argument('--pass', type=str, help='Clave del usuario')
        parser.add_argument('--rol', type=str, help='Rol del usuario [administrativo|profesional|datos|recupero]')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Creando roles y permisos ---"))
        start_roles_and_permissions()

        rol = options['rol']
        if rol == 'administrativo':
            group = Group.objects.get(name=settings.GRUPO_ADMIN)
        elif rol == 'profesional':
            group = Group.objects.get(name=settings.GRUPO_PROFESIONAL)
        elif rol == 'datos':
            group = Group.objects.get(name=settings.GRUPO_DATOS)
        elif rol == 'profesional':
            group = Group.objects.get(name=settings.GRUPO_PROFESIONAL)
        elif rol == 'recupero':
            group = Group.objects.get(name=settings.GRUPO_RECUPERO)
        else:
            raise Exception('Rol inválido')

        user = User.objects.create_user(username=options['name'], password=options['pass'])
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS("Usuario {} creado correctamente".format(options['name'])))
        