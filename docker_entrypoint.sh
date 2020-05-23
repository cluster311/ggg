#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Esperando a la BD..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 2
    done

    echo "PostgreSQL lista"
fi

# echo "Vaciar DB y correr migraciones"
python manage.py migrate

exec "$@"