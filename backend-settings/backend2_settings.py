from sensors.dev_settings import *

STATIC_ROOT = '/static'
STATIC_URL = '/static2/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/db/backend2.sqlite3',
    }
}

# For nginx reverse proxy
USE_X_FORWARDED_HOST = True
