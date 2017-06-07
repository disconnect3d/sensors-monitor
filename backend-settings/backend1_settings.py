from sensors.dev_settings import *


STATIC_ROOT = '/static'
STATIC_URL = '/static1/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/db/backend1.sqlite3',
    }
}

# For nginx reverse proxy
USE_X_FORWARDED_HOST = True
