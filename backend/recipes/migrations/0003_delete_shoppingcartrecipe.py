# Generated by Django 4.2.4 on 2023-08-21 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShoppingCartRecipe',
        ),
    ]