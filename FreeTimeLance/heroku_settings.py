from .settings import *

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'freetimelance.herokuapp.com']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'alfa3031.alfahosting-server.de'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['ALFA_EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['ALFA_EMAIL_PWD']
