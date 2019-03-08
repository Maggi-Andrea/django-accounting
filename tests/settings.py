import os
import logging

import accounting
from accounting.defaults import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "abcdef"

LANGUAGE_CODE = 'en-us'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tests._site.model_tests_app',  # contains models we need for testing
] + accounting.get_apps()

# Remove 'debug_toolbar'
try:
    INSTALLED_APPS.remove('debug_toolbar')
except ValueError:
    pass

# Add the 'tests' app, to load test models
INSTALLED_APPS.append('tests')

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] + list(accounting.ACCOUNTING_MIDDLEWARE_CLASSES)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'accounting/templates/accounting')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'accounting.apps.context_processors.metadata',
                'accounting.apps.books.context_processors.organizations',
            ],
        },
    },
]

ADMINS = ('admin@example.com',)
DEBUG = False
TEMPLATE_DEBUG = False
SITE_ID = 1


## Speed up tests

# disable logging
logging.disable(logging.CRITICAL)

# use a cheaper hashing method
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Override default fixtures folder
FIXTURE_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, '../tests/fixtures')),
)
