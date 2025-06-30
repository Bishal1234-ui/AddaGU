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
        sender_username = data['sender']
        receiver_username = data['receiver']
        is_encrypted = data.get('is_encrypted', False)
        
        # Check if users can chat with each other
        can_chat = await self.check_chat_permission(sender_username, receiver_username)
        if not can_chat:
            # Send error message back to sender
            await self.send(text_data=json.dumps({
                'error': 'Both users must follow each other to chat',
                'type': 'permission_error'
            }))
            return
        
        # Get current timestamp in IST
        current_time = timezone.now()
        
        if is_encrypted:
            # Handle encrypted message
            encrypted_message_for_sender = data.get('encrypted_message_for_sender')
            encrypted_message_for_receiver = data.get('encrypted_message_for_receiver')
            
            # Save encrypted message to database
            await self.save_encrypted_message(
                sender_username, 
                receiver_username, 
                encrypted_message_for_sender,
                encrypted_message_for_receiver,
                current_time
            )
            
            # Send encrypted message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': sender_username,
                    'receiver': receiver_username,
                    'encrypted_message_for_sender': encrypted_message_for_sender,
                    'encrypted_message_for_receiver': encrypted_message_for_receiver,
                    'is_encrypted': True,
                    'timestamp': current_time.isoformat()
                }
            )
        else:
            # Handle plain text message
            message = data['message']
            
            # Save message to database
            await self.save_message(sender_username, receiver_username, message, current_time)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender_username,
                    'receiver': receiver_username,
                    'is_encrypted': False,
                    'timestamp': current_time.isoformat()
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket with all the data
        await self.send(text_data=json.dumps({
            'message': event.get('message', ''),
            'sender': event['sender'],
            'receiver': event['receiver'],
            'timestamp': event['timestamp'],
            'is_encrypted': event['is_encrypted'],
            'encrypted_message_for_sender': event.get('encrypted_message_for_sender', ''),
            'encrypted_message_for_receiver': event.get('encrypted_message_for_receiver', '')
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message, timestamp):
        from django.contrib.auth import get_user_model
        from users.models import ChatMessage, Notification
        
        User = get_user_model()
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        
        # Create chat message (plain text)
        chat_message = ChatMessage(
            sender=sender,
            receiver=receiver,
            message=message,
            timestamp=timestamp,
            is_encrypted=False
        )
        chat_message.save()
        
        # Create notification for message
        if sender != receiver:
            Notification.objects.create(
                sender=sender,
                recipient=receiver,
                notification_type='message',
                message=f'{sender.username} sent you a message'
            )

    @database_sync_to_async
    def save_encrypted_message(self, sender_username, receiver_username, encrypted_for_sender, encrypted_for_receiver, timestamp):
        from django.contrib.auth import get_user_model
        from users.models import ChatMessage, Notification
        
        User = get_user_model()
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        
        # Create encrypted chat message
        chat_message = ChatMessage(
            sender=sender,
            receiver=receiver,
            encrypted_message_for_sender=encrypted_for_sender,
            encrypted_message_for_receiver=encrypted_for_receiver,
            timestamp=timestamp,
            is_encrypted=True
        )
        chat_message.save()
        
        # Create notification for encrypted message
        if sender != receiver:
            Notification.objects.create(
                sender=sender,
                recipient=receiver,
                notification_type='message',
                message=f'{sender.username} sent you a message'
            )

    @database_sync_to_async
    def check_chat_permission(self, sender_username, receiver_username):
        """
        Check if two users can chat with each other (both must follow each other)
        """
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)
            return sender.can_chat_with(receiver)
        except User.DoesNotExist:
            return False

