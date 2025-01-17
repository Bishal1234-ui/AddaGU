from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, Like
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from django.http import JsonResponse, HttpResponse

# for the websocket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def home_view(request):
    posts = BlogPost.objects.all()
    return render(request, 'blogs/home.html', {'posts':posts})


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

            # <<<send the new comment to the websocet>>>
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'comment_{blog_post.pk}',
                {
                    'type': 'comment_update',
                    'comment': comment.text,
                    'username': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            )
            return JsonResponse({
                'text': comment.text,
                'username': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
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