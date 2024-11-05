from django.contrib import admin

from .models import Ingredient, Recipe, GroceryItem

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(GroceryItem)
