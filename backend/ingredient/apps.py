from django.apps import AppConfig


class IngredientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingredient'
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'
