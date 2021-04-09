import os
import django

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application

from django.core.asgi import get_asgi_application
import main.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})