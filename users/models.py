from django.db import models
# import AbstractUser to add extra features to the user 
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    # email password name will be there in the User in forms.py
    # we have just added the additional needed for the profile

    def __str__(self):
        return self.username   # username is default


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.message[:50]}'
