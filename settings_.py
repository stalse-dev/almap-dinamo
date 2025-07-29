import os, io, sys, environ, firebase_admin
from pathlib import Path
from firebase_admin import credentials
from google.cloud import secretmanager

# Base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregador de envs
env = environ.Env(DEBUG=(bool, False))

# Checa se estamos rodando no GCP (ex: Cloud Run)
ON_GOOGLE_CLOUD = env("ON_GOOGLE_CLOUD", default=False)

# Se for local, carrega o .env da raiz do projeto
if not ON_GOOGLE_CLOUD:
    env.read_env(os.path.join(BASE_DIR, ".env"))
else:
    # Produção: lê o .env do Secret Manager
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "django_settings"
        project_id = "85227007031"
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("utf-8")
        env.read_env(io.StringIO(payload))
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar .env do Secret Manager: {e}")

IS_BUILD = os.environ.get("IS_BUILD") == "true"

try:
    if not firebase_admin._apps:
        if ON_GOOGLE_CLOUD:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        else:
            cred = credentials.Certificate(os.path.join(BASE_DIR, "firebase-adminsdk.json"))
        firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Firebase Admin não inicializado: {e}", file=sys.stderr)


# Configurações base do Django
SECRET_KEY = env("SECRET_KEY", default="fake-secret-key")

DEBUG = env.bool("DEBUG", default=not ON_GOOGLE_CLOUD)
ALLOWED_HOSTS = ["*"]

sys.path.append(str(BASE_DIR / "apps"))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'apps.users',  
    'apps.core',         
    'apps.dashboards',

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.core.authentication.FirebaseAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'apps.core.permissions.AllowAnyForDocsOrIsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}


CORS_ALLOW_ALL_ORIGINS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.FirebaseAuthMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_USER_MODEL = 'users.CustomUser'


if ON_GOOGLE_CLOUD:
    DB_HOST = f"/cloudsql/{env('DB_INSTANCE', default='fake-instance-id')}"
else:
    DB_HOST = env("DB_PUBLIC_IP", default="127.0.0.1")  # default local para build

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME", default="postgres"),
        'USER': env("DB_USER", default="postgres"),
        'PASSWORD': env("DB_PASSWORD", default="postgres"),
        'HOST': DB_HOST,
        'PORT': env("DB_PORT", default="5432"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# Diretório onde o collectstatic irá reunir todos os arquivos estáticos para o deploy
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
