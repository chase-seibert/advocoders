import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tbk%qsb3^no+@4vijqem0e4ql6=-%@=zuor3^k6!zl)jv6vxml'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'advocoders.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'advocoders.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.messages',
    'social_auth',
    'advocoders',
    'kombu.transport.django',
    'djcelery',
    'gunicorn',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.stackoverflow.StackoverflowBackend',
    'django.contrib.auth.backends.ModelBackend',
)

POSSIBLE_PROVIDERS = (
    'github',
    'stackoverflow',
)

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID', '782206201166.apps.googleusercontent.com')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET', 'd74bbVVjSBd59jhO9W2BM4Ix')
GOOGLE_OAUTH2_EXTRA_DATA = [
    ('link', 'link'),
    ('picture', 'picture'),
    ('name', 'name'),
    ('verified_email', 'verified_email'),
]

GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID', '98319ae893e0f9a81427')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET', '0a20d347ad146f71b221ece116f47c1d2cefb192')
GITHUB_EXTRA_DATA = [
    ('avatar_url', 'picture'),
    ('html_url', 'link'),
    ('login', 'login'),
    ('name', 'name'),
]

STACKOVERFLOW_CLIENT_ID = os.environ.get('STACKOVERFLOW_CLIENT_ID', '1123')
STACKOVERFLOW_CLIENT_SECRET = os.environ.get('STACKOVERFLOW_CLIENT_SECRET', 'Xz8hGObV1KbiglfvNv05GQ((')
STACKOVERFLOW_KEY = os.environ.get('STACKOVERFLOW_KEY', 'tMmkTZD)pXDLOga8*1NgNw((')
STACKOVERFLOW_EXTRA_DATA = [
    ('profile_image', 'picture'),
    ('link', 'link'),
    ('display_name', 'name'),
]

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/profile'
LOGIN_ERROR_URL = '/profile'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'Bro Grammer'
SOCIAL_AUTH_URLOPEN_TIMEOUT = 30
SOCIAL_AUTH_SLUGIFY_USERNAMES = True

AUTH_PROFILE_MODULE = 'advocoders.models.Profile'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BROKER_BACKEND = 'django'

import djcelery
djcelery.setup_loader()

if os.environ.get('DATABASE_URL'):
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
