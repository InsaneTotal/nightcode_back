from django.urls import path

from .consumers import OrderUpdatesConsumer

websocket_urlpatterns = [
    path('ws/orders/', OrderUpdatesConsumer.as_asgi()),
    path('ws/realtime/', OrderUpdatesConsumer.as_asgi()),
]
