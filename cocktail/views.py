
from django.shortcuts import render
from .forms import CocktailSearchForm
from .models import SearchedCocktail
from django.db.models import F
import requests

def search_cocktails(request):
    form = CocktailSearchForm()
    results = []

    if request.method == 'GET' and 'query' in request.GET:
        form = CocktailSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            cocktail, created = SearchedCocktail.objects.get_or_create(name=query)
            if created:
                cocktail.search_count = 1
            else:
                cocktail.search_count = F('search_count') + 1
            cocktail.save()

            ingredients = [i.strip() for i in query.split(',') if i.strip()]

            if len(ingredients) == 1:
                url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={ingredients[0]}'
                response = requests.get(url)
                data = response.json()
                results = data.get('drinks', [])
            else:
                cocktails_sets = []
                for ingredient in ingredients:
                    url = f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}'
                    response = requests.get(url)
                    data = response.json()
                    drinks = data.get('drinks', [])
                    if isinstance(drinks, list):
                     cocktails_sets.append({d['idDrink']: d for d in drinks})


                if cocktails_sets:
                    common_ids = set(cocktails_sets[0].keys())
                    for s in cocktails_sets[1:]:
                        common_ids &= set(s.keys())

                    results = [cocktails_sets[0][cid] for cid in common_ids]

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

def popular_cocktails(request):
    cocktails = SearchedCocktail.objects.all()
    return render(request, 'cocktail/popular.html', {'cocktails': cocktails})

