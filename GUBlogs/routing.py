# Create a routing.py file in your app directory to define WebSocket routes.

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/like/<int:post_id>/', consumers.LikeConsumer.as_asgi()),
    path('ws/comment/<int:post_id>/', consumers.CommentConsumer.as_asgi()),
]