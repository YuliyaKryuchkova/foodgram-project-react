from rest_framework import viewsets

from ingredient.models import Ingredient
from .filters import IngredientFilter
from .pagination import LimitPageNumberPagination
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = []
    pagination_class = LimitPageNumberPagination
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)
