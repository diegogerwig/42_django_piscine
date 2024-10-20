from django import forms
from django.contrib.auth import get_user_model
from .models import Tip
from django.contrib.auth import authenticate

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    verif_password = forms.CharField(required=True, widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        verif_password = cleaned_data.get('verif_password')
        
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', "The name entered is already taken")
        
        if password and verif_password and password != verif_password:
            self.add_error('password', "The password must be identical in the 2 password fields")
            self.add_error('verif_password', "The password must be identical in the 2 password fields")
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        
        return cleaned_data

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your tip here...'}),
        }

