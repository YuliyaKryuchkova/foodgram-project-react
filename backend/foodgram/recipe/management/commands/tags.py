import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipe.models import Tag


class Command(BaseCommand):
    help = 'Загрузить список тегов'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR
        with open(
                f'{data_path}/data/tags.csv',
                'r',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            if Tag.objects.first():
                self.stdout.write(self.style.SUCCESS('Данные списка тегов уже есть'))
                return
            Tag.objects.bulk_create(
                Tag(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
