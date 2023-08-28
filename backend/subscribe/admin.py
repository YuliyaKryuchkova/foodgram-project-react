from django.contrib import admin

from subscribe.models import Subscribe


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    search_fields = (
        'user__email',
        'author__email',
    )
    empty_value_display = '-пусто-'
