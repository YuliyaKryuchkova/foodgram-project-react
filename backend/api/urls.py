from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .api_favorite.views import favorite
from .api_ingredient.views import IngredientViewSet
from .api_recipe.views import RecipeViewSet
from .api_shopcart.views import shopping_cart
from .api_subscribe.views import subscribe
from .api_tag.views import TagViewSet
from .api_users.views import CustomDjoserUserViewSet

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
    path(
        'users/<int:id>/subscribe/',
        subscribe),
    # path(
    #     'recipes/<int:pk>/favorite/',
    #     favorite),
    path(
        'recipes/<int:pk>/shopping_cart/',
        shopping_cart),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
