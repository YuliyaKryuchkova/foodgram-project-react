from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomDjoserUserViewSet

router = DefaultRouter()

router.register(
    'users',
    CustomDjoserUserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
