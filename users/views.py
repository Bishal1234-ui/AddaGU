
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# we need blog post to get the blog of a specific user
from blogs.models import BlogPost
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse


def signup_view(request):
    # Checks if the HTTP request method is POST,
    #  which means the form has been submitted.
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')

    # If the request method is not POST, it means the form has not 
    # been submitted yet, so it initializes an empty form.   
    else:
        form = CustomUserCreationForm()
    return render(request,'users/signup.html', {'form':form})


# for login we will use a default authentication form
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()  # login the user
            login(request,user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})



# create the profile vieew
@login_required
def profile_view(request):
    # get the post by user using a filter by author
    user_posts = BlogPost.objects.filter(author=request.user)
    context = {
        'user':request.user,
        'user_posts':user_posts
        }
    return render(request, 'users/profile.html', context)


# edit the profile

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


## to view other use profile
@login_required
def user_profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_posts = BlogPost.objects.filter(author=user)
    is_following = request.user.following.filter(username=username).exists()
    context = {
        'user_profile':user,
        'user_posts':user_posts,
        'is_following':is_following
    }
    return render(request, 'users/user_profile.html', context)

# follow unfollow 
@login_required
def follow_unfollow_view(request, username):
    user_to_follow = get_object_or_404(CustomUser,username=username)
    if request.user.following.filter(username=username).exists():
        request.user.following.remove(user_to_follow)
    else:
        request.user.following.add(user_to_follow)

    return redirect('user_profile',username=username)

# to view the followers and following list
@login_required
def followers_list_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    followers = user.followers.all()
    followers_data = [{'username': follower.username, 'profile_picture': follower.profile_picture.url if follower.profile_picture else None} for follower in followers]
    return JsonResponse({'followers': followers_data})

@login_required
def following_list_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    following = user.following.all()
    following_data = [{'username': follow.username, 'profile_picture': follow.profile_picture.url if follow.profile_picture else None} for follow in following]
    return JsonResponse({'following': following_data})

@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('profile')
    else:
        return HttpResponse("You are not allowed to delete this post.")
