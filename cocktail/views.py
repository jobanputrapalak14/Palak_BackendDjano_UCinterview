import requests
from django.shortcuts import render
from .forms import CocktailSearchForm

def search_cocktails(request):
    form = CocktailSearchForm()
    results = []

    if request.method == 'GET' and 'query' in request.GET:
        form = CocktailSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}'
            response = requests.get(url)
            data = response.json()
            results = data.get('drinks', [])

    return render(request, 'cocktail/search.html', {
        'form': form,
        'results': results
    })

def cocktail_detail(request, cocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
    response = requests.get(url)
    data = response.json()
    cocktail = None
    ingredients = []

    if data['drinks']:
        cocktail = data['drinks'][0]

        # Get first 3 ingredients and measures
        for i in range(1, 4):
            ingredient = cocktail.get(f"strIngredient{i}")
            measure = cocktail.get(f"strMeasure{i}")
            if ingredient:
                ingredients.append({
                    'ingredient': ingredient,
                    'measure': measure
                })

    return render(request, 'cocktail/detail.html', {
        'cocktail': cocktail,
        'ingredients': ingredients
    })

