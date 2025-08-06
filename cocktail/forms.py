# cocktail/forms.py

from django import forms

class CocktailSearchForm(forms.Form):
    query = forms.CharField(label='Search for a cocktail or ingredient', max_length=100)
