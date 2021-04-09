import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application

from django.core.asgi import get_asgi_application
import main.routing
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
  "http": get_default_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})