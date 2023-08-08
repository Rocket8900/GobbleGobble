from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = 'static/'


MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]