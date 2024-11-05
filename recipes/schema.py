import typing
import strawberry

from .types import Ingredient, Recipe, GroceryItem
from .models import Ingredient as IngredientModel
from .models import Recipe as RecipeModel
from .models import GroceryItem as GroceryItemModel

def get_ingredients():
    return [i for i in IngredientModel.objects.all()]

def get_recipes():
    recipes = [r for r in RecipeModel.objects.all()]
    return [
        Recipe(
            id=r.id,
            name=r.name,
            calories=r.calories,
            steps=r.steps,
            ingredients=[Ingredient(id=i.id, name=i.name) for i in r.ingredients.all()]
        ) for r in recipes
    ]

def get_grocery_list():
    grocery_list = [g for g in GroceryItemModel.objects.all()]
    return [
        GroceryItem(
            id=g.id,
            ingredient=g.ingredient.name,
            count=g.quantity,
        ) for g in grocery_list
    ]

@strawberry.type
class Query:
    ingredients: typing.List[Ingredient] = strawberry.field(resolver=get_ingredients)
    recipes: typing.List[Recipe] = strawberry.field(resolver=get_recipes)
    grocery_list: typing.List[GroceryItem] = strawberry.field(resolver=get_grocery_list)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_recipe(name: str, ingredients: typing.List[str]) -> Recipe:
        ingredient_objects = []
        for ingredient_name in ingredients:
            ingredient_objects.append(IngredientModel.objects.get_or_create(name=ingredient_name)[0])
        recipe = RecipeModel(name=name)
        recipe.save()
        recipe.ingredients.set(ingredient_objects)
        recipe.save()
        return Recipe(
            id=recipe.id,
            name=recipe.name,
            calories=recipe.calories,
            steps=recipe.steps,
            ingredients=[Ingredient(id=i.id, name=i.name) for i in recipe.ingredients.all()]
        )

    @strawberry.mutation
    def add_item_to_grocery_list(item_name: str) -> GroceryItem:
        item = GroceryItemModel.objects.add_to_list(item_name)
        return GroceryItem(
            id=item.id,
            ingredient=item.ingredient.name,
            count=item.quantity
        )

    @strawberry.mutation
    def add_recipe_to_grocery_list(recipe_name: str) -> typing.List[GroceryItem]:
        items = GroceryItemModel.objects.add_recipe_to_list(recipe_name)
        return [
            GroceryItem(
                id=g.id,
                ingredient=g.ingredient.name,
                count=g.quantity,
            ) for g in items
        ]

    @strawberry.mutation
    def check_item_off_grocery_list(item_name: str) -> GroceryItem:
        item = GroceryItemModel.objects.check_off_list(item_name)
        return GroceryItem(
            id=item.id,
            ingredient=item.ingredient.name,
            count=item.quantity
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)
