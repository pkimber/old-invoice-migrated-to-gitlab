# -*- encoding: utf-8 -*-
from example_invoice.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'temp.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# http://docs.celeryproject.org/en/2.5/django/unit-testing.html
CELERY_ALWAYS_EAGER = True
