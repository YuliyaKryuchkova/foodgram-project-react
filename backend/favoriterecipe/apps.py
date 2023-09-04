from django.apps import AppConfig


class FavoriterecipeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'favoriterecipe'
    verbose_name = 'Избранный'
    verbose_name_plural = 'Избранные'
