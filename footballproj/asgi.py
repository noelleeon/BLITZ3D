"""
ASGI config for footballproj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fbapp'))
from fbapp.routing import websocket_urlpatterns
from django.urls import re_path
from fbapp import consumers
import django
#https://stackoverflow.com/questions/74180849/web-sockets-failing-connection-django-channels
#https://channels.readthedocs.io/en/stable/tutorial/part_2.html
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'footballproj.settingsprod')

django_asgi_app = get_asgi_application()

from fbapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
   "https": django_asgi_app,
   "websocket": AllowedHostsOriginValidator(
      AuthMiddlewareStack(
        URLRouter(
          websocket_urlpatterns,
        )
      )
    ),
})

ASGI_APPLICATION = 'footballproj.asgi.application'
