import os

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "cookie_consent",
    "testapp",
]
SITE_ID = 1

ROOT_URLCONF = "testapp.urls"

DEBUG = True

STATIC_URL = "/static/"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

SECRET_KEY = "2n6)=vnp8@bu0om9d05vwf7@=5vpn%)97-!d*t4zq1mku%0-@j"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.path.dirname(__file__), "database.db"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MIDDLEWARE_CLASSES = MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_MAX_AGE = 60 * 60 * 24 * 365 * 1  # 1 year
COOKIE_CONSENT_LOG_ENABLED = True
