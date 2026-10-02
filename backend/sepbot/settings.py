import os
import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Load environment variables
load_dotenv(os.path.join(BASE_DIR.parent, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-sepbot-secret-key-change-in-production-2026')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'https://app11.tanchonhomserverxxx.online,http://localhost:8000,http://127.0.0.1:8000'
    ).split(',') if origin.strip()
]

# Support HTTPS behind reverse proxies (Nginx Proxy Manager / Traefik / Cloudflare)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'rest_framework',
    'corsheaders',
    'django_celery_beat',

    # Local Apps
    'accounts',
    'assessment',
    'health',
    'knowledge',
    'faq',
    'linebot',
    'notification',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sepbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sepbot.wsgi.application'

# Database configuration
# PostgreSQL for both Docker and Local Mac environment
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
IS_DOCKER = os.path.exists('/.dockerenv') or os.getenv('IS_DOCKER', 'False').lower() == 'true'

# If running outside Docker container and host is set to 'db', fallback to localhost
if not IS_DOCKER and DB_HOST == 'db':
    DB_HOST = 'localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'sepbot_db'),
        'USER': os.getenv('POSTGRES_USER', 'sepbot_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'sepbot_password'),
        'HOST': DB_HOST,
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'th-th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True

# Celery Settings
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'send-daily-check-reminder-at-9am': {
        'task': 'notification.tasks.send_daily_check_reminder',
        'schedule': crontab(hour=9, minute=0),
    },
    'send-vital-sign-reminder-day14-30-at-9am': {
        'task': 'notification.tasks.send_vital_sign_reminder_day14_30',
        'schedule': crontab(hour=9, minute=0),
    },
}

# LINE API Credentials
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_LIFF_ID_REGISTER = os.getenv('LINE_LIFF_ID_REGISTER', '')
LINE_LIFF_ID_DAILY_CHECK = os.getenv('LINE_LIFF_ID_DAILY_CHECK', '')
LINE_LIFF_ID_SCREENING = os.getenv('LINE_LIFF_ID_SCREENING', '')
LINE_LIFF_ID_VITAL_SIGN = os.getenv('LINE_LIFF_ID_VITAL_SIGN', '')
NURSE_LINE_USER_ID = os.getenv('NURSE_LINE_USER_ID', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '').strip()
