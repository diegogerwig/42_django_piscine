from django import forms
from .models import Movies


class RemoveForm(forms.Form):
    title = forms.ChoiceField(choices=(), required=True)

    def __init__(self, choices, *args, **kwargs):
        super(RemoveForm, self).__init__(*args, **kwargs)
        self.fields['title'].choices = choices


class UpdateForm(forms.Form):
    select = forms.ChoiceField(choices=[], required=True)
    opening_crawl = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select'].choices = [(movie.episode_nb, f"Episode {movie.episode_nb}: {movie.title}") for movie in Movies.objects.all().order_by('episode_nb')]

