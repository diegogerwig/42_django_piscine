from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Username',
            'style': 'width: 150px;',
            'maxlength': '20'
        }),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Password',
            'style': 'width: 150px;',
            'maxlength': '20'
        }),
        label=''
    )