from django.urls import path
from .views import *

urlpatterns = [
    path('', messages_page, name='messages-page'),
    path('message-to/<int:pk>', create_thread, name='messages-to'),
]
