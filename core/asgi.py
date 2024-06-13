# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import get_asgi_application after setting the environment variable
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from vehicle.consumers import VehicleLocationConsumer

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter([
        path('ws/vehicle_location/', VehicleLocationConsumer.as_asgi()),
    ]),
})
