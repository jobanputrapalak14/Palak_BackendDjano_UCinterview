# cocktail/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_cocktails, name='search_cocktails'),
    path('cocktail/<int:cocktail_id>/', views.cocktail_detail, name='cocktail_detail'),

]
