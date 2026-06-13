from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production-xyz123'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'students',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'student_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'student_portal.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hour

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FastAPI Backend Configuration
FASTAPI_BASE_URL = "http://127.0.0.1:8000"
FASTAPI_API_KEY = "laptop-key-123"

# Anthropic AI — get your key at https://console.anthropic.com
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"

# Google Gemini AI — get your key at https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "AQ.Ab8RN6LQxoWYLZN-VA1kTxhdNjv-TLe_Js_p7ewEvAfEuKXJWw"

# Google Gemini AI — get your key at https://aistudio.google.com/apikey
# GEMINI_API_KEY = "your-gemini-api-key-here"

# Portal Users — { "username": "password" }
# New users registered via /register/ are appended here automatically.
PORTAL_USERS = {
    "admin": "admin123",
}
