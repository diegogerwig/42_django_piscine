from django import forms
from django.forms.widgets import HiddenInput
from ex.models import Article, UserFavouriteArticle


class FavouriteForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), widget=forms.HiddenInput())

    def __init__(self, article=None, *args, **kwargs):
        if article and 'initial' not in kwargs:
            kwargs['initial'] = {'article': article}
        super().__init__(*args, **kwargs)