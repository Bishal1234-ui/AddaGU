from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, Like
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Count

# for the websocket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()

def create_notification(sender, recipient, notification_type, message, blog_post=None):
    """
    Helper function to create notifications
    """
    if sender != recipient:  # Don't create notifications for self-actions
        from users.models import Notification
        Notification.objects.create(
            sender=sender,
            recipient=recipient,
            notification_type=notification_type,
            message=message,
            blog_post=blog_post
        )

# @login_required
def home_view(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('blog_post_id', flat=True)

    for post in posts:
        post.liked = post.pk in liked_posts
    
    # Get statistics for the welcome section
    total_users = User.objects.count()
    total_likes = Like.objects.count()
    
    return render(request, 'blogs/home.html', {
        'posts': posts,
        'total_users': total_users,
        'total_likes': total_likes,
    })


# toggle the like
@login_required
def toggle_like(request, pk):
    blog_post = get_object_or_404(BlogPost,pk=pk)
    user = request.user
    liked  = False
    # 1. Attempts to get an existing Like object for the combination of 
    # blog_post and user. If it doesn't exist, it creates a new one.
    # 2. 'created' is a boolean that is True if a new Like was created, 
    # and False if an existing Like was retrieved.
    like,created = Like.objects.get_or_create(blog_post=blog_post, user= user)
    if not created:   # like already exist by that user
        # delete the like
        like.delete()
    else:
        # or else make Liked = true ( like will alread be crated in above line )
        liked = True
        
        # Create notification for like
        create_notification(
            sender=user,
            recipient=blog_post.author,
            notification_type='like',
            message=f'{user.username} liked your post "{blog_post.title}"',
            blog_post=blog_post
        )

    # Send the updated like count to the WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'like_{blog_post.pk}',
        {
            'type': 'like_update',
            'likes_count': blog_post.likes.count()
        }
    )

    return JsonResponse({'liked': liked, 'likes_count':blog_post.likes.count()})


def blog_detail_view(request, pk):
    # retrive the blog post by its primary key
    blog_post = get_object_or_404(BlogPost, pk =pk)

    # <<<comment handling part >>>>
    # retrive all the comments realted to a blogpost ( realted using 'comments')
    comments = blog_post.comments.all()
    if request.method == 'POST':
        # Extract the comment text from the POST data
        comment_text = request.POST.get('text')
        # if the comment is submmitedd we create the Comment object and upload to dtabase
        if comment_text:
            comment = Comment.objects.create(blog_post=blog_post, author=request.user, text=comment_text )

            # Create notification for comment
            create_notification(
                sender=request.user,
                recipient=blog_post.author,
                notification_type='comment',
                message=f'{request.user.username} commented on your post "{blog_post.title}"',
                blog_post=blog_post
            )

            # <<<send the new comment to the websocet>>>
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'comment_{blog_post.pk}',
                {
                    'type': 'comment_update',
                    'comment': comment.text,
                    'username': comment.author.username,
                    'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p'),
                    'comment_id': comment.id
                }
            )
            return JsonResponse({
                'text': comment.text,
                'username': comment.author.username,
                'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p'),
                'comment_id': comment.id
            })

            # Redirect to the same blog detail page to show the new comment
           # return redirect('blog_detail', pk=blog_post.pk)

    # <<< >>>>

    # << Like handling >>
    liked  = False
    if request.user.is_authenticated:
        liked = blog_post.likes.filter(user=request.user).exists()

    # retrieve all likes from the blogpost
    likes = blog_post.likes.all()

    return render(request, 'blogs/blog_detail.html', {
        'post':blog_post, 
        'comments':comments,
        'likes':likes,
        'liked': liked
        })



@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('home')
    else:
        form = BlogPostForm()

    return render(request, 'blogs/create_post.html',{'form':form})


# delete comment views
@login_required

# delete a specific comment based on its id. ( the id wil be defined in the html page)
def delete_comment(request, comment_id):

    
    
    comment = get_object_or_404(Comment, id = comment_id)
    # if the user is not the comment author
    if request.user != comment.author:
        return HttpResponse("You are not allowed to delete someone's comment")
    
    comment.delete()
    return JsonResponse({'success': True, 'comment_id':comment_id})