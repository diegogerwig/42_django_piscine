from django import forms

class History(forms.Form):
    history = forms.CharField(
        label='📝 Your message (max 50 characters)',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Max 50 characters'})
    )

    def clean_history(self):
        data = self.cleaned_data['history']
        if len(data) > 50:
            raise forms.ValidationError("The message is too long.")
        return data
