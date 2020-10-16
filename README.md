[![Build Status](https://travis-ci.org/cluster311/ggg.svg?branch=master)](https://travis-ci.org/cluster311/ggg)

# Sistema abierto de información de la Salud

Propuesto por la Municipalidad de Córdoba y con la
financiación de la Organización Mundial de la Salud
nace este sistema abierto de información para la salud.

## Manual

Versión en desarrollo del manual [aquí](https://docs.google.com/document/d/1ePgRHtQiG81u2eF4qf48ozq4RMyviwgu/export?format=pdf)

## Modulos libres 

 - Modulo SISA/PUCO: https://github.com/cluster311/sisa
 - Modulo SSS: https://github.com/cluster311/sss-beneficiarios
 - Modulo impresion Anexo II: https://github.com/cluster311/Anexo2/
 - Modulo CIE10: https://github.com/cluster311/cie10
 - Modulo Nomenclador HPGD: https://github.com/cluster311/nhpgd
 - Modulo base de Obras Sociales: https://github.com/cluster311/obras-sociales-argentinas

## Cargar con datos de prueba

```bash
./manage.py import_centros_salud_cba
./manage.py start_permissions
./manage.py create_test_users
./manage.py create_test_data
./manage.py create_test_paciente_data

```
## Como contribuir

Como contribuir con este proyecto abierto:

Crear un PR contra la rama predeterminada _develop_.
