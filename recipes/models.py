from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)
    calories = models.IntegerField(default=0)
    steps = models.JSONField(default='[]')

    def __str__(self):
        return self.name


class GroceryListManager(models.Manager):
    def add_to_list(self, item_name):
        ingredient = Ingredient.objects.get_or_create(name=item_name)[0]
        item = self.model.objects.get_or_create(ingredient_id=ingredient.id)[0]
        item.quantity = item.quantity + 1
        item.save()
        return item

    def add_recipe_to_list(self, recipe_name):
        ingredients = []
        recipe = Recipe.objects.get_or_create(name=recipe_name)[0]
        for item in recipe.ingredients.all():
            ingredients.append(self.add_to_list(item.name))
        return ingredients

    def check_off_list(self, item_name):
        ingredient = Ingredient.objects.get_or_create(name=item_name)[0]
        item = self.model.objects.get_or_create(ingredient_id=ingredient.id)[0]
        try:
            ingredient = Ingredient.objects.get(name=item_name)
            item = self.model.objects.get(ingredient_id=ingredient.id)
            item.quantity = 0
            item.save()
            return item
        except ObjectDoesNotExist:
            return

class GroceryItem(models.Model):
    ingredient = models.OneToOneField('Ingredient', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    objects=GroceryListManager()

    def __str__(self):
        return '{name}, {quantity}'.format(
            name=self.ingredient.name,
            quantity=self.quantity,
        )
