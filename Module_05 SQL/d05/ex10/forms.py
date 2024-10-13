from django import forms
from django.core.exceptions import ValidationError
from .models import People

class MovieSearchForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date')
    max_release_date = forms.DateField(label='Movies maximum release date')
    planet_diameter = forms.IntegerField(label='Planet diameter greater than', min_value=0)
    character_gender = forms.ChoiceField(label='Character gender', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gender_choices = [('', 'all')]  # 'all' en minúsculas
        gender_choices += [(g.lower(), g.lower()) for g in People.objects.values_list('gender', flat=True).distinct() if g]
        self.fields['character_gender'].choices = gender_choices

    def clean_planet_diameter(self):
        diameter = self.cleaned_data.get('planet_diameter')
        if diameter is not None and diameter < 0:
            raise ValidationError("Planet diameter must be greater than or equal to zero.")
        return diameter

