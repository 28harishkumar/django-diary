# Parse database configuration from $DATABASE_URL
DATABASES = {

    'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_name',
        'USER':'database_user',
        'PASSWORD':'database_user_password',
        'HOST':'database_host',
        'PORT': '5432',
        }, 
    
}

SECRET_KEY = 'your secret key'

SECURE_SSL_REDIRECT = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
