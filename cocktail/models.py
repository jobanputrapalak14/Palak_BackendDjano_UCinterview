from django.db import models

# Create your models here.
class SearchedCocktail(models.Model):
    name = models.CharField(unique=True)  
    search_count = models.PositiveIntegerField(default=0)  
