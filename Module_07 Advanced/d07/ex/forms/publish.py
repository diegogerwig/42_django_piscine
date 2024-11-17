from django import forms
from django.forms.widgets import Textarea

class PublishForm(forms.Form):
    title = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title'
        })
    )
    
    synopsis = forms.CharField(
        max_length=312,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a brief synopsis'
        })
    )
    
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your article content here',
            'rows': 10
        })
    )