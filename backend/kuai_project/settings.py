import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()  # Loads .env from BASE_DIR

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SECURITY
# ==============================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-this-before-production"
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ==============================
# APPLICATIONS
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'imagekit',
    'django_filters',

    # Local apps
    'core',
    'about',
    'news',
    'events',
    'projects',
    'team',
    'gallery',
    'partners',
    'contact',
    'indabax',
]

# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================
# URLS & TEMPLATES
# ==============================
ROOT_URLCONF = 'kuai_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'kuai_project.wsgi.application'

# ==============================
# DATABASE
# ==============================
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', ''),
        
        # ADDED: Connection pooling settings for Supabase
        'CONN_MAX_AGE': 300,  # Reuse connections for 5 minutes (300 seconds)
        'CONN_HEALTH_CHECKS': True,  # Check connection health before reuse
        
        # ADDED: Additional options for better connection management
        'OPTIONS': {
            'connect_timeout': 10,  # 10 second connection timeout
            'options': '-c statement_timeout=30000',  # 30 second query timeout
        },
    }
}

# Support DATABASE_URL for production (Render, Railway, etc.)
if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=300,  # UPDATED: Increased from 600 to 300 for better turnover
        conn_health_checks=True,
    )
    # ADDED: Ensure OPTIONS are preserved when using DATABASE_URL
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
        'options': '-c statement_timeout=30000',
    }

# ==============================
# PASSWORD VALIDATION
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# INTERNATIONALIZATION
# ==============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

# ==============================
# STATIC & MEDIA FILES
# ==============================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Only add static dir if it exists
STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

# WhiteNoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================
# DEFAULT PRIMARY KEY
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# CORS SETTINGS
# ==============================
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# ==============================
# REST FRAMEWORK
# ==============================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ==============================
# SECURITY SETTINGS FOR PRODUCTION
# ==============================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'




















































# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # ==============================
# # LOAD ENV VARIABLES
# # ==============================
# load_dotenv()  # Loads .env from BASE_DIR

# BASE_DIR = Path(__file__).resolve().parent.parent

# # ==============================
# # SECURITY
# # ==============================
# SECRET_KEY = os.getenv(
#     "SECRET_KEY",
#     "django-insecure-change-this-before-production"
# )

# DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "kabailab.com,www.kabailab.com").split(",")

# # ==============================
# # APPLICATIONS
# # ==============================
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     # Third-party apps
#     'rest_framework',
#     'corsheaders',
#     'imagekit',
#     'django_filters',

#     # Local apps
#     'core',
#     'about',
#     'news',
#     'events',
#     'projects',
#     'team',
#     'gallery',
#     'partners',
#     'contact',
#     'indabax',
# ]

# # ==============================
# # MIDDLEWARE
# # ==============================
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # ==============================
# # URLS & TEMPLATES
# # ==============================
# ROOT_URLCONF = 'kuai_project.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'kuai_project.wsgi.application'

# # ==============================
# # DATABASE
# # ==============================
# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
#         'USER': os.getenv('DB_USER', ''),
#         'PASSWORD': os.getenv('DB_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', ''),
#     }
# }

# # ==============================
# # PASSWORD VALIDATION
# # ==============================
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ==============================
# # INTERNATIONALIZATION
# # ==============================
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Kampala'
# USE_I18N = True
# USE_TZ = True

# # ==============================
# # STATIC & MEDIA FILES
# # ==============================
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
#     BASE_DIR / 'frontend_build' / 'static',  # React static files
# ]

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # ==============================
# # DEFAULT PRIMARY KEY
# # ==============================
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ==============================
# # CORS SETTINGS
# # ==============================
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "https://kabailab.com",
#     "https://www.kabailab.com",
# ]
# CORS_ALLOW_CREDENTIALS = True

# # ==============================
# # REST FRAMEWORK
# # ==============================
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,
# }