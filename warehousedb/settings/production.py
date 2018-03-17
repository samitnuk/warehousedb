from .base import *

DEBUG = False

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ls.DB_NAME,
        'USER': ls.DB_USER,
        'PASSWORD': ls.DB_PASSWORD,
        'HOST': ls.DB_HOST,
        'PORT': ls.DB_PORT
    }
}
