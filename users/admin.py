from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ChatMessage, Notification
from .forms import CustomUserCreationForm, CustomUserChangeForm


# here we create a admin and register both the model and form

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'bio', 'profile_picture', 'is_staff', 'is_active']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'timestamp', 'is_read']
    list_filter = ['timestamp', 'is_read']
    search_fields = ['sender__username', 'receiver__username', 'message']
    readonly_fields = ['timestamp']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']

admin.site.register(CustomUser,CustomUserAdmin)



