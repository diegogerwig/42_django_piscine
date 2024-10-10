from django import forms
from .models import People

class MovieSearchForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date')
    max_release_date = forms.DateField(label='Movies maximum release date')
    planet_diameter = forms.IntegerField(label='Planet diameter greater than')
    character_gender = forms.ChoiceField(label='Character gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gender_choices = People.objects.values_list('gender', flat=True).distinct()
        self.fields['character_gender'].choices = [(g, g) for g in gender_choices if g]

