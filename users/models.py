from django.db import models
# import AbstractUser to add extra features to the user 
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    # email password name will be there in the User in forms.py
    # we have just added the additional needed for the profile

    def __str__(self):
        return self.username   # username is default


