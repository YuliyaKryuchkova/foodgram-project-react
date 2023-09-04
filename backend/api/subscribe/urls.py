from django.urls import path

from .views import subscribe, subscriptions

urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        subscribe),
    path(
        'users/subscriptions/',
        subscriptions),
]
