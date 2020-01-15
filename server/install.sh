
# Ubutnu 18.04 LTS
sudo apt update
sudo apt install -y python3-venv postgresql postgresql-contrib postgis python-psycopg2 libpq-dev gcc python3-dev supervisor nginx

cd ~
python3 -m venv env
source env/bin/activate
git clone https://github.com/cluster311/ggg.git
cd ggg
pip install -r requirements.txt
pip install -r prod_requirements.txt

# database
sudo su - postgres
psql
# definir credenciales seguras
CREATE USER ggg_user WITH PASSWORD 'ggg_pass';
ALTER ROLE ggg_user SUPERUSER;
CREATE EXTENSION postgis;
CREATE DATABASE ggg_db OWNER ggg_user;

# add to local_settings.py
ALLOWED_HOSTS = ['lala.com']
DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': 'ggg_db',
         'USER': 'ggg_user',
         'PASSWORD': 'ggg_pass',
         'HOST': 'localhost'
    },
}

./manage.py migrate
./manage.py createsuperuser

cd server
# gunicorn
sudo mkdir /etc/gunicorn/
sudo cp gunicorn/ggg.conf.py /etc/gunicorn/

# supervisor
sudo cp supervisor/ggg.conf /etc/supervisor/conf.d/
sudo supervisorctl reload
sudo supervisorctl start ggg

# nginx
sudo cp nginx/cache.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/cache.conf /etc/nginx/sites-enabled/cache.conf

sudo cp nginx/ggg.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ggg.conf /etc/nginx/sites-enabled/ggg.conf

# test
sudo nginx -t
sudo systemctl restart nginx

# check URL: works
# ready to deploy
./deploy.sh

# agregar HTTPS
sudo add-apt-repository ppa:certbot/certbot
sudo apt install -y python-certbot-nginx
sudo certbot --nginx -d lala.com

# etapa 2, GeoDjango
sudo apt install binutils libproj-dev gdal-bin

# obtener un API KEY de google y agregarlo a local_settings como GOOGLE_API_KEY

Importar datos

Al iniciar se requiere tener algunos datos cargados a la base.
 - Los códigos CIE se importan automáticamente con el migrate de la librería
 - Los códigos del Nomenclador de Hospitales Públicos de Gestión Descentralizada no 
   son obligatorios y por lo tanto pueden cargarse con la función 
   importar_desde_nomenclador de la clase TipoPrestacion de la app de Recupero:
    TipoPrestacion.importar_desde_nomenclador()
 - Las Obras Sociales se cargan con la funcion startdb de la clase ObraSocial. Por ahora no esta agregado al migrate: ObraSocial.startdb()
 - Importar Profesionales: ./manage.py import_profesionales. Comando hecho 
   específicamente para los profesionales de córdoba (la base no está 
   publicada en el repositorio)
 - Centros de salud de Córdoba ciudad: ./manage.py import_centros_salud_cba. 
   Los datos están abiertos y en el repo, son públicos.