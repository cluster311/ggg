[![Build Status](https://travis-ci.org/cluster311/ggg.svg?branch=master)](https://travis-ci.org/cluster311/ggg)

# Sistema abierto de información de la Salud

Propuesto por la Municipalidad de Córdoba y con la
financiación de la Organización Mundial de la Salud
nace este sistema abierto de información para la salud.

## Manual

Versión en desarrollo del manual [aquí](https://docs.google.com/document/d/1ePgRHtQiG81u2eF4qf48ozq4RMyviwgu/export?format=pdf)

## Objetivo del sistema

Objetivos del sistema:

## Como usarlo

Instrucciones de instalación y uso:

-   Clonar el repositorio

```bash
git clone https://github.com/cluster311/ggg
```

## Con Docker

0. Instalar [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)

1.  Hacer ejecutable el script `docker_entrypoint.sh`
    ```bash
    # Linux
    chmod +x docker_entrypoint.sh
    ```

2.  Levantar los 2 contenedores (web y db).

    -   `--build` construye las imagenes antes de levantar el contenedor.
    -   `-d` "desconecta" nuestra terminal del proceso.
    -   Además se corren las migraciones (`docker_entrypoint.sh`)

    ```bash
    docker-compose up -d --build
    ```

    -   Para probar el sistema ir a http://localhost:8000

    -   Se pueden ver los logs ejecutando
    ```bash
    docker-compose logs 
    ```

3.  Cargar los datos restantes

    Lo haremos manualmente en una shell de Django dentro del contenedor.

    1.  Conectarse al contenedor:

    ```bash
    # `web` es el nombre del servicio con nuestra app de Django.
    docker-compose exec web bash
    ```

    2. Una vez dentro del contenedor, en la carpeta `/code`, ejecutar `./manage.py shell_plus`
    3. Siguiendo la sección **Importar datos** del [manual](https://docs.google.com/document/d/1ePgRHtQiG81u2eF4qf48ozq4RMyviwgu/edit#heading=h.aq1beefkoxs9):

    ```python
    TipoPrestacion.importar_desde_nomenclador()
    ObraSocial.startdb()
    ```

    4. Salir de la shell de Django y ejecutar:

    ```bash
    ./manage.py import_centros_salud_cba
    ./manage.py start_permissions
    ./manage.py create_test_users
    ./manage.py create_test_data
    ./manage.py create_test_paciente_data

    ```

    5. Crear un superusuario (Opcional)

    ```bash
    ./manage.py createsuperuser
    ```

    6. `exit` para cerrar la shell dentro del contenedor.


-   Para detener los contenedores ejecutar `docker-compose stop`.

## Como contribuir

Como contribuir con este proyecto abierto:

Crear un PR contra la rama predeterminada _develop_.
