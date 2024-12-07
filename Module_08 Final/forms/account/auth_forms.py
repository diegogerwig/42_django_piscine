from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=150)
    password = forms.CharField(min_length=6)
    confirm_password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken')
        return username

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data