from .settings import *

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DEBUG=True

ALLOWED_HOSTS = ['0.0.0.0']