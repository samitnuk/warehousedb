from .base import *

DEBUG = False

ALLOWED_HOSTS = ['10.0.0.10']

SECRET_KEY = 'qm#xb=ea=w_70-wy0=#^$g=$@5!pbc7s3=$eupv2bpo7rf&u3k'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'warehouse',
        'USER': 'warehouse_user',
        'PASSWORD': 'super_secret',
        'HOST': 'localhost',
        'PORT': '',
    }
}
