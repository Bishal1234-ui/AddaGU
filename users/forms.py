from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm( UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'profile_picture')

        # this are used to modify the form using bootstrap
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label

class CustomUserChangeForm( UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_picture')

# now we register our model in admin.py