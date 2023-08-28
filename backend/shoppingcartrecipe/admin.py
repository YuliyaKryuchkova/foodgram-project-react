from django.contrib import admin

from shoppingcartrecipe.models import ShoppingCartRecipe


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
