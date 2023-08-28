from django.contrib import admin

from favoriterecipe.models import FavoriteRecipe


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
