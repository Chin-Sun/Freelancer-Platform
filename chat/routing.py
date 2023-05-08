from django.urls import path
from . import consumer

websocket_utlpatterns = [
    path('chat/', consumer.ChatConsumer.as_asgi()),
    path('chat/message-to/<int:pk>', consumer.ChatConsumer.as_asgi())
]