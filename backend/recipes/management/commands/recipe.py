import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from ingredient.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузить список ингридиентов'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR
        try:
            with open(
                    f'{data_path}/data/ingredients.csv',
                    'r', encoding='utf-8'
            ) as file:
                reader = csv.DictReader(file)
                if Ingredient.objects.first():
                    self.stdout.write(self.style.SUCCESS(
                        'Данные списка ингридиентов уже есть')
                    )
                    return
                Ingredient.objects.bulk_create(Ingredient(**data) for data in reader)
            self.stdout.write(self.style.SUCCESS('Данные загружены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка загрузки: {e}'))
