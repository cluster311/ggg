# Imagen oficial Python
FROM python:3.8

# Preparar el directorio para la app
WORKDIR /code

# Set env variables
# https://docs.python.org/3/using/cmdline.html#id1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Instalar dependencias para geodjango
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin netcat \
    && rm -rf /var/lib/apt

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip
COPY ./*requirements.txt /code/
RUN pip install -r requirements.txt -r dev-requirements.txt

# Copiar el proyecto (/ggg)
COPY . /code/

# Run entrypoint
ENTRYPOINT [ "/code/docker_entrypoint.sh"]