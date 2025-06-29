import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


# Create a consumers.py file in your 
# app directory to handle WebSocket connections.

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'like_{self.post_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        likes_count = data['likes_count']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'like_update',
                'likes_count': likes_count
            }
        )

    async def like_update(self, event):
        likes_count = event['likes_count']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'likes_count': likes_count
        }))


## handle websocket connection for comments

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'comment_{self.post_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        comment = data['comment']
        username = data['username']
        created_at = data['created_at']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_update',
                'comment': comment,
                'username': username,
                'created_at': created_at
            }
        )

    async def comment_update(self, event):
        comment = event['comment']
        username = event['username']
        created_at = event['created_at']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'username': username,
            'created_at': created_at
        }))


## for chat functionality

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']
        receiver_username = data['receiver']

        # Save message to database
        await self.save_message(sender_username, receiver_username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        from django.contrib.auth import get_user_model
        from users.models import ChatMessage
        
        User = get_user_model()
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )

