"""
WSGI config for opendoor_interview project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opendoor_interview.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import sklearn
#from dj_static import Cling

#application = Cling(get_wsgi_application())
