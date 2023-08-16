from django.contrib import admin

from .models import Ingredient, Tag, Recipe, IngredientRecipe, FavoriteRecipe, ShoppingCartRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'measurement_unit',
                    )
    search_fields = ('name',
                     'measurement_unit',
                     )
    list_filter = (
        'name',
    )
    ordering = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'text',
        'pub_date'
    )
    search_fields = (
        'name',
        'cooking_time'
    )
    list_filter = (
        'pub_date',
    )

    inlines = [IngredientRecipeInline]

    ordering = (
        'pub_date',
    )
    empty_value_display = '-пусто-'


@admin.register(FavoriteRecipe)
class FavoriteRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'user'
    )
    ordering = (
        'user',
    )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCartRecipe)
class ShoppingCartRecipe(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )
    list_filter = (
        'recipe',
        'user'
    )
    search_fields = (
        'user',
    )
    ordering = (
        'user',
    )
    empty_value_display = '-пусто-'
