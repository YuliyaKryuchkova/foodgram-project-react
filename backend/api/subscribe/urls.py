from django.urls import path

from .views import subscribe, subscriptions

urlpatterns = [
    path(
        'users/subscriptions/',
        subscriptions),
    path(
        'users/<int:id>/subscribe/',
        subscribe),
]
