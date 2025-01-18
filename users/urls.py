from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('profile/<str:username>/follow_unfollow/', views.follow_unfollow_view, name='follow_unfollow'),
    path('profile/<str:username>/followers/', views.followers_list_view, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list_view, name='following_list'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]