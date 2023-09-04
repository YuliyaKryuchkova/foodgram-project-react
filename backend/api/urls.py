from django.urls import include, path

app_name = 'api'


urlpatterns = [
    path('', include('api.tag.urls')),
    path('', include('api.subscribe.urls')),
    path('', include('api.users.urls')),
    path('', include('api.shopcart.urls')),
    path('', include('api.recipe.urls')),
    path('', include('api.ingredient.urls')),
    path('', include('api.favorite.urls')),
]
