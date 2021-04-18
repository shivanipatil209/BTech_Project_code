from django import forms

class SearchForm(forms.Form):
    search_words = forms.CharField(max_length=100)
