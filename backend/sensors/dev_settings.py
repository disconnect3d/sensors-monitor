from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0=t_dl#wk8g6)yd&qpk2a%htb_3^lda3=t7!^(-16e_gyxqdc@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CORS settings #TODO/FIXME: Change on production
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ('*',)
CORS_ORIGIN_REGEX_WHITELIST = ('*', '.*')


default_db_path = os.path.join(BASE_DIR, 'db.sqlite3')
db_path = os.environ.get('DJANGO_APP_DB_PATH', default_db_path)
print('DB PATH: "%s"' % db_path)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db_path,
    }
}
