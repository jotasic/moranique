from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('SQL_DATABASE'),
        'USER': get_env_variable('SQL_USER'),
        'PASSWORD': get_env_variable('SQL_PASSWORD'),
        'HOST': get_env_variable('SQL_HOST'),
        'PORT': get_env_variable('SQL_PORT'),
    }
}

SECRET_KEY = get_env_variable('DJANGO_SECRECT_KEY')

DEBUG = True