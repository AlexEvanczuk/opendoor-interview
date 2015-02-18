"""
WSGI config for opendoor_interview project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opendoor_interview.settings")
#settings.configure()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#from whitenoise.django import DjangoWhiteNoise
#application = DjangoWhiteNoise(application)
