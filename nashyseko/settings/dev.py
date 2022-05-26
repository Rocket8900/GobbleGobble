from .base import *

SECRET_KEY = 'django-insecure-de^a9nt!y+xav@_hq@*xb^eo^t#(c+ozl_4t85$tic#o#3pg2g'

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = 'static/'

# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]