
from django.urls import path
from .views import home_view, blog_detail_view, create_post_view, toggle_like, delete_comment

urlpatterns = [
    path('', home_view, name='home'),
    path('post/<int:pk>/', blog_detail_view, name='blog_detail'),
    path('post/<int:pk>/toggle_like/', toggle_like, name='toggle_like'),
    path('create/', create_post_view, name='create_post'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment')

]