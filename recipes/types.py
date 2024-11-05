import typing
import strawberry


@strawberry.type()
class Ingredient:
    id: int
    name: str

@strawberry.type()
class Recipe:
    id: int
    name: str
    calories: int
    steps: str
    ingredients: typing.List[Ingredient]

@strawberry.type()
class GroceryItem:
    id: int
    ingredient: str
    count: int
