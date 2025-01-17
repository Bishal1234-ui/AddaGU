from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


# here we create a admin and register both the model and form

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'bio', 'profile_picture', 'is_staff', 'is_active']

admin.site.register(CustomUser,CustomUserAdmin)



