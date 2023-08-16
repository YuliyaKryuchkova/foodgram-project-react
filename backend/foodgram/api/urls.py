from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet,
                    TagViewSet,
                    IngredientViewSet,
                    CustomDjoserUserViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(
    'users',
    CustomDjoserUserViewSet,
    basename='users'
)
router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router.register(
    'tags',
    TagViewSet,
    basename='tags'
)
router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
