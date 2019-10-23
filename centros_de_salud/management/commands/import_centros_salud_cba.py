"""
Importar los centros de salud desde el mapa oficial de la Ciudad de Córdoba
https://www.google.com/maps/d/kml?mid=1vKX3YVLV4u3jLvMu22WqhYjrUzM
"""
# !/usr/bin/python

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.gis.geos import GEOSGeometry
from centros_de_salud.models import CentroDeSalud
import sys
from fastkml import kml


class Command(BaseCommand):
    help = """Comando para importar centros de salud"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path del archivo KML local',
            default='centros_de_salud/resources/centros-de-salud-cba.kml'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando carga'))

        path = options['path']
        f = open(path, 'rt', encoding='utf-8')
        doc = f.read()
        f.close()
        k = kml.KML()
        k.from_string(doc)
        count = 0
        errores = []

        features = list(k.features())

        barrios = 0  # barrios descargados a la base de datos
        for feature in features:
            self.stdout.write("=============================")
            self.stdout.write("Doc: {}".format(feature.name))
            self.stdout.write("=============================")

            folders = list(feature.features())

            for folder in folders:
                self.stdout.write("=============================")
                self.stdout.write("Folder: {}".format(folder.name))
                self.stdout.write("=============================")

                places = list(folder.features())
                for place in places:
                    count += 1
                    """ ejemplo:
                    <name>CS N° 1 - General Mosconi</name>
                        <description>
                            <![CDATA[Calle Pedro Naon 1330
                                <br>Atención 7 - 21 hs<br>TE: 4335102 / 5428
                            ]]>
                        </description>
                        <styleUrl>#icon-22</styleUrl>
                        <Point>
                        <coordinates>
                            -64.149057,-31.3648,0
                        </coordinates>
                        </Point>
                    """
                    self.stdout.write(" -- Place: {}".format(place.name))
                    self.stdout.write(" -- - Descr: {}".format(
                        place.description
                    ))

                    pt = place.geometry
                    # es un pygeoif.geometry.Point
                    # POINT (-64.136987 -31.417331 0.0)
                    self.stdout.write(" -- - Point: {}".format(pt))

                    cs, created = CentroDeSalud.objects.get_or_create(
                        nombre=place.name
                    )
                    cs.descripcion = place.description
                    # esto tampoco funca
                    # ubicacion = GEOSGeometry(pt.wkt)
                    ubicacion = GEOSGeometry(
                        f'POINT({pt.x} {pt.y})',
                        srid=4326
                    )
                    self.stdout.write(" -- - Ubic: {}".format(ubicacion))
                    cs.ubicacion = ubicacion

                    cs.save()

        txt = f'Se procesaron {count} centros'
        self.stdout.write(self.style.SUCCESS(txt))
        txt = f'Errores: {errores}'
        self.stdout.write(self.style.ERROR(txt))
