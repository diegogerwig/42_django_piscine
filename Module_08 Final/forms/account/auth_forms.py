from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        min_length=3,
        max_length=150,
        error_messages={
            'required': 'Username is required',
            'min_length': 'Username must be at least 3 characters',
            'max_length': 'Username must be 150 characters or less'
        }
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        error_messages={
            'required': 'Password is required',
            'min_length': 'Password must be at least 6 characters'
        }
    )
    confirm_password = forms.CharField(
        required=True,
        error_messages={
            'required': 'Password confirmation is required'
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username is required')
            
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken')
            
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match')
                
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        error_messages={
            'required': 'Username is required'
        }
    )
    password = forms.CharField(
        required=True,
        error_messages={
            'required': 'Password is required'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not username or not password:
            raise ValidationError('Both username and password are required')
            
        return cleaned_data