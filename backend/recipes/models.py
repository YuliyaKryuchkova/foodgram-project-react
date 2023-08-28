from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import MinValueValidator
from django.db import models

from ingredient.models import Ingredient
from tag.models import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        'Название рецепта',
        max_length=150
    )
    image = models.ImageField(
        upload_to='recipes',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты для рецепта',
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления не менее 1 минуты'),
        )
    )
    pub_date = models.DateTimeField(
        'Дата добавления рецепта',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes')
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов'),),
        verbose_name='Количество', )

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'
