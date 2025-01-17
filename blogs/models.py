from django.db import models

# SETTINGS IS USED TO GET THE AUTHENTICATION USER AS AUTHOR
from django.conf import settings


class BlogPost(models.Model):
    # author of  a blog will be the customuser
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blogimage = models.ImageField(upload_to='blogimages/',blank=True,null=True)

    def __str__(self):
        return self.title


## for comment add a comment model

class Comment(models.Model):
    # for comment BlogPost is the foreignkey
    blog_post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    # author of the comment is the User who is comment ( login user)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog_post}'
    

## like functionality mode

class Like(models.Model):
    # create a similar many to one relationship (like comments) with a BlogPost
    blog_post = models.ForeignKey(BlogPost, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Meta class holds additional information about the Like model
    class Meta:
        # ensure that each user can only like a specific blog post once. The combination 
        # of blog_post and user must be unique in the database.
        unique_together = ('blog_post','user')

    def __str__(self):
        return f'liked by {self.user} on {self.blog_post}'
