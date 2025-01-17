
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

# we need blog post to get the blog of a specific user
from blogs.models import BlogPost
from django.contrib.auth.decorators import login_required


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

