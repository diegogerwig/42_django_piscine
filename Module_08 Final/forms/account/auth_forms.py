from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is required')
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already taken')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and len(password) < 6:
            raise ValidationError({'password': 'Password must be at least 6 characters'})
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError({'confirm_password': 'Passwords do not match'})
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)