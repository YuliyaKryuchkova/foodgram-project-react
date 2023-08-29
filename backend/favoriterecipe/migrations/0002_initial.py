# Generated by Django 4.2.4 on 2023-08-21 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        ('favoriterecipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorited', to='recipes.recipe'),
        ),
    ]