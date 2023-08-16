import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipe.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузить ингридиенты'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR
        with open(
                f'{data_path}/data/ingredients.csv',
                'r',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            if Ingredient.objects.first():
                self.stdout.write(self.style.SUCCESS(
                    'Данные ингредиентов уже есть')
                )
                return
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
