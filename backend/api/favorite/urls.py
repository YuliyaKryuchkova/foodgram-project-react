from django.urls import path

from .views import favorite

urlpatterns = [
    path(
        'recipes/<int:pk>/favorite/',
        favorite),
]
