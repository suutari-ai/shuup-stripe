# -*- coding: utf-8 -*-
import os
import tempfile

SECRET_KEY = "x"


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "easy_thumbnails",
    "filer",
    "shoop.core",
    "shoop.simple_pricing",
    "shoop.default_tax",
    "shoop_stripe",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(
            tempfile.gettempdir(),
            'shoop_stripe_tests.sqlite3'
        ),
    }
}


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


MIGRATION_MODULES = DisableMigrations()
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "var", "media")
