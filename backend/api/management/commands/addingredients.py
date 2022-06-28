import json

from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    help = 'Add list of ingredients in database'

    def handle(self, *args, **options):
        with open('ingredients.json', 'r', encoding='utf-8') as file:
            igredients_list = json.load(file)

        ingredient_objs = [
            Ingredient(name=igredient['name'],
                       measurement_unit=igredient['measurement_unit'])
            for igredient in igredients_list
        ]

        Ingredient.objects.bulk_create(ingredient_objs)

        print('Данные успешно добавлены.')
