from django.urls import path

from .views import shopping_cart


urlpatterns = [
    path(
        'recipes/<int:pk>/shopping_cart/',
        shopping_cart),
]
