from django.urls import re_path
from .consumers import MySocket
websocket_urlpatterns = [    
    re_path(r'ws/', MySocket.as_asgi())
]