# !/usr/bin/python
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from core.base_permission import create_test_users, start_roles_and_permissions


class Command(BaseCommand):
    help = """Crear los grupos y permisos iniciales"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Creando roles y permisos ---"))
        start_roles_and_permissions()
        ret = create_test_users()

        self.stdout.write(self.style.SUCCESS(f"Usuarios creados: {ret}"))