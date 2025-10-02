import os
from .settings import *

# PythonAnywhere settings
DEBUG = False
ALLOWED_HOSTS = ['yusuftrg13.pythonanywhere.com', 'localhost', '127.0.0.1']

# Database for PythonAnywhere (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yusuftrg13$portfolioblog',
        'USER': 'yusuftrg13',
        'PASSWORD': 'your_db_password_here',
        'HOST': 'yusuftrg13.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yusuftrg13/portfolio_blog/staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yusuftrg13/portfolio_blog/media'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Secret key - you'll need to set this on PythonAnywhere
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key-for-pythonanywhere-123456')

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}