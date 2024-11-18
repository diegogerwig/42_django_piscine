from django import forms
from ex.models import Article

class PublishForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'synopsis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief synopsis'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your article content here',
                'rows': 10
            })
        }