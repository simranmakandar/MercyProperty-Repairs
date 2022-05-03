"""
WSGI config for MAH_V5 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MAH_V5.settings')

application = get_wsgi_application()

# import os
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MAH_V5.settings")
#
# from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise
#
# application = get_wsgi_application()
# application = DjangoWhiteNoise(application)
