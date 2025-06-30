from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('profile/<str:username>/follow_unfollow/', views.follow_unfollow_view, name='follow_unfollow'),
    path('profile/<str:username>/followers/', views.followers_list_view, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list_view, name='following_list'),
    path('delete_post/<int:pk>/', views.delete_post_view, name='delete_post'),
    path('chat/', views.chat_list_view, name='chat_list'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('api/unread-count/', views.get_unread_count, name='get_unread_count'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notification-count/', views.get_notification_count, name='get_notification_count'),
    path('api/mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('api/mark-all-notifications-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]