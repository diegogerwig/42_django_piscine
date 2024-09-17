from django import forms

class History(forms.Form):
    histo = forms.CharField(label='histo')
