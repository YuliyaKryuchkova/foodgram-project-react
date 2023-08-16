from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=254
    )
    measurement_unit = models.CharField(
        verbose_name='Еденица измерения',
        max_length=150
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_measurement_unit'
            )
        ]

    def __str__(self):
        return (f'{self.name},'
                f'{self.measurement_unit},'
                )


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=150
    )
    color = models.CharField(
        'Цвет',
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        'Ссылка',
        max_length=150,
        unique=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор')
    name = models.CharField(
        'Название рецепта',
        max_length=150
    )
    image = models.ImageField(
        upload_to='recipes',
        null=True,
        blank=True
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты для рецепта',
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipe'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(1),)
    )
    pub_date = models.DateTimeField(
        'Дата добавления рецепта',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
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
                1, message='Количество ингридиентов'),),
        verbose_name='Количество',)

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Юзер')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited')

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_is_favorited')
        ]

    def __str__(self):
        return f'{self.recipe} - {self.user}'


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Юзер')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart')

    class Meta:
        verbose_name = 'ShoppingCartRecipe'
        verbose_name_plural = 'ShoppingCartRecipes'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shoppingcart')
        ]

    def __str__(self):
        return f'{self.recipe} - {self.user}'
