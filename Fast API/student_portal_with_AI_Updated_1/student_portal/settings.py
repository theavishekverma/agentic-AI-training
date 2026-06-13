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
ANTHROPIC_API_KEY = "API Key"

# Google Gemini AI
# If your key starts with "AIza" → paste it as GEMINI_API_KEY, leave GEMINI_PROJECT_ID empty
# If your key starts with "AQ"   → paste it as GEMINI_API_KEY AND set GEMINI_PROJECT_ID
#   (find your project ID at https://console.cloud.google.com → select project → copy ID)
GEMINI_API_KEY    =  "API Key"
#"AQ.Ab8RN6IYbMeqAGEGOFiqOUBkT7pk4J6Wc18O1Ze-AftNa6h4OQ"
GEMINI_PROJECT_ID = "Project ID"   # required only for AQ keys e.g. "my-project-123456"

# Portal Users — { "username": "password" }
# New users registered via /register/ are appended here automatically.
PORTAL_USERS = {
    "admin": "admin123",
}
