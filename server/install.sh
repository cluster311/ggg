
# Ubutnu 18.04 LTS
sudo apt update
sudo apt install -y python3-venv postgresql postgresql-contrib postgis python-psycopg2 libpq-dev gcc python3-dev supervisor

cd ~
python3 -m venv env
source env/bin/activate
git clone https://github.com/cluster311/ggg.git
cd ggg
pip install -r requirements.txt

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
cp gunicorn/ggg.conf.py /etc/gunicorn/

# supervisor
cp supervisor/ggg.conf /etc/supervisor/conf.d/
sudo supervisorctl start ggg

# nginx
sudo cp nginx/cache.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/cache.conf /etc/nginx/sites-available/cache.conf

sudo cp nginx/ggg.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ggg.conf /etc/nginx/sites-available/ggg.conf
