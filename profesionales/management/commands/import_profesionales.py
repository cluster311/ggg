"""
Importar la base de datos de profesionales que nos proveen desde excel

Muestra de los datos
AFILIADO    NOMBRE	    PROFESION           DOCUMENTO	ESTADO
42000	    JUAN PEREZ  MEDICO VETERINARIO  5556460     OBLIGADO
15000	    JUANA PEREZ MEDICO              55553961	OBLIGADO

TELEFONO	    DOMICILIO	    BARRIO  LOCALIDAD	    DEPARTAMENTO    VOTA
03555-555555   	CHACO 31        MARINO  RIO CEBALLOS    COLON           S
                SAAVEDRA 1069           RIO CEBALLOS    COLON           S
"""
# !/usr/bin/python

from django.core.management.base import BaseCommand
from django.db import transaction
from profesionales.models import Profesional
import sys
import pyexcel as pe


class Command(BaseCommand):
    help = """Comando para importar profesionales de la salud"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            help="Path del archivo XLS local",
            default="profesionales/resources/PADRONACTIVOS2.xls",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("--- Comenzando carga, por favor espere ---")
        )
        fieldnames = [
            "AFILIADO",
            "NOMBRE",
            "PROFESION",
            "DOCUMENTO",
            "ESTADO",
            "TELEFONO",
            "DOMICILIO",
            "BARRIO",
            "LOCALIDAD",
            "DEPARTAMENTO",
            "VOTA",
        ]

        path = options["path"]

        count = 0
        matriculas = []
        dnis = []
        errores = []

        book = pe.get_book(file_name=path)

        for sheet in book:

            for fila in sheet:
                self.stdout.write(self.style.SUCCESS(f"importando {fila}"))
                row = {
                    "AFILIADO": fila[0],
                    "NOMBRE": fila[1],
                    "PROFESION": fila[2],
                    "DOCUMENTO": fila[3],
                    "ESTADO": fila[4],
                    "TELEFONO": fila[5],
                    "DOMICILIO": fila[6],
                    "BARRIO": fila[7],
                    "LOCALIDAD": fila[8],
                    "DEPARTAMENTO": fila[9],
                }

                self.stdout.write(self.style.SUCCESS(f"importando {row}"))

                # Es un número!
                dni = row['DOCUMENTO']  # .strip().replace('.', '')
                if dni in dnis:
                    error = f"DNI DUPLICADO: {dni} en {row}"
                    self.stdout.write(self.style.ERROR(error))
                    # sys.exit(1)
                    errores.append(error)
                    continue

                matricula = row["AFILIADO"]
                if matricula in matriculas:
                    error = f"Matricula DUPLICADa: {matricula} en {row}"
                    self.stdout.write(self.style.ERROR(error))
                    # sys.exit(1)
                    errores.append(error)
                    continue

                dnis.append(dni)
                matriculas.append(matricula)

                p, created = Profesional.objects.get_or_create(
                    numero_documento=dni
                )
                p.importar_matriculado(row=row)
                p.save()

                count += 1

            txt = f"Se procesaron {count} profesionales"
            self.stdout.write(self.style.SUCCESS(txt))
            txt = f"Errores: {errores}"
            self.stdout.write(self.style.ERROR(txt))
