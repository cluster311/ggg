# GGG
Sistema de gestión de historias clínicas.


## Instalación

### Requisitos
1. [Python 3.7](https://www.python.org/downloads/)
1. [PostgreSQL](https://www.postgresql.org/)
1. [GDAL](https://gdal.org/)
1. [Docker](https://www.docker.com/)
1. [Docker-Compose](https://docs.docker.com/compose/)

### Pasos a seguir
1. Clonar repositorio: `git clone git@gitlab.com:cluster311/ggg.git`.
1. Levantar la base de datos: `docker-compose up db`.
1. Cambiar al usuario postgres y conectarse a la base de datos: `sudo su - postgres; psql`.
1. Crear usuario **ggg_user** con contraseña **ggg_pass**: `CREATE USER ggg_user SUPERUSER WITH PASSWORD 'ggg_pass';`.
1. Crear base de datos **ggg_db**: `CREATE DATABASE ggg_db WITH OWNER ggg_user;`.
1. Volver a tu usuario e instalar las dependencias: `pip install -r requirements.txt`.
1. Correr las migraciones: `python manage.py migrate`.
1. Levantar el docker del Django: `docker-compose up web`.
1. La app estará disponible en la url: `http://localhost:8000`
