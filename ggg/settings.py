import os

VERSION = '1.2.111'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6di0*fi)^us0rf!a#e0*-c_y!!ip%f_vsp+0xitzshaah#&g4w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    # 'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'tinymce',
    'address',
    'cie10_django',
    'crispy_forms',
    'tempus_dominus',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # our apps
    'core',
    'obras_sociales',
    'pacientes',
    'profesionales',
    'centros_de_salud',
    'nhpgd_django',  # nomenclador de hostpitales publicos de gestion descentralizada
    'calendario',
    'recupero',
    'usuarios',
    'especialidades',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ggg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'ggg', 'templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ggg.context_processors.cpp_settings',
                'usuarios.context_processors.cpp_usuarios',
            ],
        },
    },
]

WSGI_APPLICATION = 'ggg.wsgi.application'


# to fill in local_settings.py or use like this for travis CI
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_NAME', 'test_db'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432")
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Ver https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# for prod env ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# LOGIN_URL = 'una-url'
LOGIN_REDIRECT_URL = 'admin.home'

SOCIALACCOUNT_QUERY_EMAIL = True

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

GOOGLE_API_KEY = 'xxx'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
PRIVATE_FILES_ROOT = os.path.join(BASE_DIR, 'file_private')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'ggginfo.log',
            'formatter': 'verbose'
        },
 
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'cie10_django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# contacto settings
CARACTERISTICA_TELEFONO_DEFAULT = '351'     # CORDOBA
CARACTERISTICA_DEFAULT = '351'

# para obtener datos oficiales de las obras sociales de las personas vía SISA
# https://pypi.org/project/sisa/
os.environ['USER_SISA'] = ''
os.environ['PASS_SISA'] = ''
CACHED_OSS_INFO_SISA_SECONDS = 60 * 60 * 24 * 30  # 30 dias de cache para info de las OSS de los pacientes

SOURCE_OSS_SISA = 'SISA'
SOURCE_OSS_SSSALUD = 'SSSalud'
SOURCE_OSS_SSS = 'SSS'


USER_SSS = 'FAKE'
PASS_SSS = 'FAKE'
REVISE_DATA_DAYS = 60

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Titulo o nombre de este sistema
SYS_SHORT_TITLE = 'HCD/R'
SYS_TITLE = 'HCD/R[ecupero]'
SYS_DESCRIPTION = 'Sistema de información de salud para historia clínica y recupero de gasto en Argentina'
SYS_LOGO = '/static/sys_logo.png'

# dummy to avoid errors
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Option: django-ses with AWS
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
# EMAIL_PORT = 2587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = <my-ses-smtp-username>
# EMAIL_HOST_PASSWORD = <my-ses-smtp-password>


LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'landing'

# ------------------------------------------
# Grupos y permisos iniciales de cada uno --
# ------------------------------------------
# Ciudadano que usa los servicios de salud
GRUPO_CIUDADANO = 'grupo_ciudadano'
# Empleados administrativos del municipio
GRUPO_ADMIN = 'grupo_administrativo'
# Profesionales médicos que dan servicios en el municipio
GRUPO_PROFESIONAL = 'grupo_profesional'
# Analistas de datos
GRUPO_DATOS = 'grupo_datos'
# Administradores generales (acceso a modificar las listas base)
GRUPO_SUPER_ADMIN = 'grupo_super_admin'
# Recupero de gasto
GRUPO_RECUPERO = 'grupo_recupero'

# ------------------------------------------
# ------------------------------------------
try:
    from .local_settings import *
except:
    pass
