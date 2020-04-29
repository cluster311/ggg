# !/usr/bin/python

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
import sys
import pyexcel as pe

from core.base_permission import create_test_paciente_data


class Command(BaseCommand):
    help = """Crear los pacientes"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Creando datos para pruebas ---"))
        create_test_paciente_data()
        self.stdout.write(self.style.SUCCESS("--- datos creados ---"))
