from models import Post
from django import forms
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("user", "views")
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Body'}),
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = {'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        }