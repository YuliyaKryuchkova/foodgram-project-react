from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter
from .pagination import LimitPageNumberPagination
from .serializers import (RecipeCreateUpdateSerializer,
                          RecipeRetriveListSerializer)
from recipes.models import IngredientRecipe, Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list',):
            return RecipeRetriveListSerializer
        return RecipeCreateUpdateSerializer

    # def message_shopping_cart(self, ingredients):
    #     shopping_list = 'Список продуктов:'
    #     for ingredient in ingredients:
    #         shopping_list += (
    #             f"\n{ingredient['ingredient__name']} "
    #             f"({ingredient['ingredient__measurement_unit']}) - "
    #             f"{ingredient['amount']}")
    #     file = 'shopping_list.txt'
    #     response = HttpResponse(shopping_list, content_type='text/plain')
    #     response['Content-Disposition'] = f'attachment; filename="{file}.txt"
    #     return response
    #
    # @action(detail=False, methods=['GET'])
    # def download_shopping_cart(self, request):
    #     ingredients = IngredientRecipe.objects.filter(
    #         recipe__shoppingcart__user=request.user
    #     ).order_by('ingredient__name').values(
    #         'ingredient__name', 'ingredient__measurement_unit'
    #     ).annotate(amount=Sum('amount'))
    #     return self.message_shopping_cart(ingredients)
    @action(detail=False, methods=['GET'])
    def download_shopping_cart(request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shoppingcart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        shopping_cart_data = {
            'ingredients': list(ingredients)
        }

        return JsonResponse(shopping_cart_data)
