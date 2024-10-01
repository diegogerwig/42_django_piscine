from django import forms

class RemoveForm(forms.Form):
    title = forms.ChoiceField(choices=(), required=True)

    def __init__(self, choices, *args, **kwargs):
        super(RemoveForm, self).__init__(*args, **kwargs)
        self.fields['title'].choices = choices

class UpdateForm(forms.Form):
    title = forms.ChoiceField(choices=(), required=True)
    opening_crawl = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, choices=None, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['title'].choices = choices
