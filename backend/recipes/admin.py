from django.contrib import admin

from .models import Recipe, IngredientRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'text',
        'pub_date',
        'get_favorite_count'
    )
    search_fields = (
        'name',
        'cooking_time',
        'tags',
        'pub_date'
    )
    list_filter = (
        'pub_date',
    )
    inlines = [IngredientRecipeInline]
    filter_horizontal = (
        'tags',
    )

    ordering = (
        'pub_date',
    )
    empty_value_display = '-пусто-'

    @admin.display(
        description='Колличество добавлений в избранное'
    )
    def get_favorite_count(self, obj):
        return obj.is_favorited.count()
