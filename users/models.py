from django.db import models
# import AbstractUser to add extra features to the user 
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Q, Max, Count, Case, When, IntegerField
from .encryption import encrypt_for_user, decrypt_for_user

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    # email password name will be there in the User in forms.py
    # we have just added the additional needed for the profile

    def __str__(self):
        return self.username   # username is default
    
    def get_conversations(self):
        """
        Get all conversations for this user with unread message counts
        """
        from django.db.models import Q, Subquery, OuterRef
        
        # Get all users this user has chatted with
        conversations = CustomUser.objects.filter(
            Q(sent_messages__receiver=self) | Q(received_messages__sender=self)
        ).exclude(
            id=self.id
        ).distinct()
        
        # Add unread message count for each conversation
        result = []
        for user in conversations:
            # Get unread messages from this user to current user
            unread_count = ChatMessage.objects.filter(
                sender=user,
                receiver=self,
                is_read=False
            ).count()
            
            # Get the latest message between these users
            latest_message = ChatMessage.objects.filter(
                Q(sender=self, receiver=user) | Q(sender=user, receiver=self)
            ).order_by('-timestamp').first()
            
            result.append({
                'user': user,
                'unread_count': unread_count,
                'latest_message': latest_message
            })
        
        # Sort by latest message timestamp
        result.sort(key=lambda x: x['latest_message'].timestamp if x['latest_message'] else timezone.now(), reverse=True)
        return result
    
    def get_total_unread_count(self):
        """
        Get total unread message count for this user
        """
        return ChatMessage.objects.filter(receiver=self, is_read=False).count()


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField(blank=True, null=True)  # For plain text messages
    encrypted_message_for_sender = models.TextField(blank=True, null=True)  # Encrypted message that sender can decrypt
    encrypted_message_for_receiver = models.TextField(blank=True, null=True)  # Encrypted message that receiver can decrypt
    timestamp = models.DateTimeField(default=timezone.now)
    is_encrypted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        if self.is_encrypted:
            return f'{self.sender.username} to {self.receiver.username}: [Encrypted Message]'
        else:
            return f'{self.sender.username} to {self.receiver.username}: {self.message[:50]}...'
    
    def set_message(self, plain_message):
        """
        Encrypt and store the message.
        The message is encrypted with both sender's and receiver's keys.
        """
        # Store the encrypted message
        self.message = encrypt_for_user(plain_message, self.sender.id)
    
    def get_message_for_user(self, user):
        """
        Decrypt and return the message for a specific user.
        Both sender and receiver should be able to read the message.
        """
        if user.id == self.sender.id or user.id == self.receiver.id:
            # Since we encrypt with sender's key, always use sender's key to decrypt
            try:
                return decrypt_for_user(self.message, self.sender.id)
            except:
                return "[Message could not be decrypted]"
        else:
            return "[Access denied]"
    
    def get_plain_message(self):
        """
        Get the decrypted message using sender's key.
        This is used for displaying messages in the chat.
        """
        return decrypt_for_user(self.message, self.sender.id)
