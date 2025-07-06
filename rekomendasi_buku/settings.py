import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Pengaturan Keamanan Utama ---
# Variabel ini WAJIB diatur di Railway
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Atur variabel ALLOWED_HOSTS di Railway, pisahkan dengan koma
# Contoh: .railway.app,domaincustom.com
ALLOWED_HOSTS_str = config('ALLOWED_HOSTS', default='127.0.0.1,localhost')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_str.split(',')]

CSRF_TRUSTED_ORIGINS_str = config('CSRF_TRUSTED_ORIGINS', default='')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_str.split(',')]

# Pastikan cookie hanya dikirim melalui HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# --- Definisi Aplikasi ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Untuk development, tapi aman ditinggal
    'django.contrib.staticfiles',
    'sistem', # Koma yang hilang sudah ditambahkan
]

# --- Middleware ---
# Pastikan whitenoise ada setelah SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rekomendasi_buku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rekomendasi_buku.wsgi.application'


# --- Konfigurasi Database ---
# Hanya gunakan blok ini. Blok database yang lama (hardcoded) dihapus.
# Konfigurasi diambil dari variabel DATABASE_URL di Railway.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# --- Validasi Password ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internasionalisasi ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta' # Disesuaikan ke zona waktu Indonesia
USE_I18N = True
USE_TZ = True


# --- Pengaturan File Statik (CSS, JS, Gambar) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- Tipe Primary Key Default ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Pengaturan API Kustom ---
# Gunakan config() agar konsisten
GOOGLE_BOOKS_API_KEY = config('GOOGLE_BOOKS_API_KEY', default='')