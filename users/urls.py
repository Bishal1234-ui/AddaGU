from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]