# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from ingredient.models import Ingredient
from .filters import IngredientFilter
from .serializers import IngredientSerializer
from api.permissions import IsAuthorOrReadOnly


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)
