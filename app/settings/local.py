DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret key'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER':'user',
        'PASSWORD':'password',
        'HOST':'127.0.0.1',
        'PORT': '3306',
        },
}
