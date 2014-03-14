"""
Django settings for checkin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import imp, os

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Private settings
if ON_OPENSHIFT:
    DB_NAME = os.environ['OPENSHIFT_APP_NAME']
    DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
    DB_PASSWORD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    DB_PORT = os.environ['DB_OPENSHIFT_POSTGRESQL_DB_PORTPORT']
else:
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# Make a dictionary of default keys
default_keys = { 'SECRET_KEY': '^a1b2c3d4e5f6-' }
# Replace default keys with dynamic values if we are in OpenShift
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)

# Make this unique, and don't share it with anybody.
SECRET_KEY = use_keys['SECRET_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    DEBUG = bool(os.environ.get('DEBUG', False))
    if DEBUG:
        print('WARNING: The DEBUG environment is set to True.')
else:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = [
    'checkin.gogreenstreets.org', 
    'greenstreets.mapc.org', 
    'greenstreetsinitiative.org',
    'checkin-greenstreets.rhcloud.com',
]


# Application definition
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'qrcode',
    'south',
    'debug_toolbar',

    # Project apps
    'survey',
    'leaderboard',
    'leaderboardlist',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # FIXME: leaderboard dosn't include CSRF
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Grappelli requirement (?)
# TEMPLATE_CONTEXT_PROCESSORS += (
#     'django.core.context_processors.request',
# )
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Media files (user uploads, etc.)
MEDIA_URL = '/media/'
if ON_OPENSHIFT:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
if ON_OPENSHIFT:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
