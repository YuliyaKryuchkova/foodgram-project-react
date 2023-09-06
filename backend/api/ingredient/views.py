from rest_framework import viewsets

from api.permissions import IsAuthorOrReadOnly
from ingredient.models import Ingredient
from .filters import IngredientFilter
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)
