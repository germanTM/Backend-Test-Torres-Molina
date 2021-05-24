import pytest

from .models import Ingredient

@pytest.fixture
def ingredient_factory(db):
    def create_ingredient(name: str):
        ingredient = Ingredient.objects.create(name=name)
        return ingredient
    return create_ingredient

def new_ingredient(db, ingredient_factory):
    return ingredient_factory("ajo")