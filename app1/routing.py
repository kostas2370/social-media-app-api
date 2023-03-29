from django.urls import path
from .consumers import ChatConsumer
ws_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi())
]
