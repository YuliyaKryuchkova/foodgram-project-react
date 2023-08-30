from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.permissions import IsAuthorOrReadOnly
from rest_framework.response import Response

from .filters import RecipeFilter
from .pagination import LimitPageNumberPagination
from .serializers import (RecipeCreateUpdateSerializer,
                          RecipeRetriveListSerializer, FavoriteSerializer)
from recipes.models import IngredientRecipe, Recipe

from favoriterecipe.models import FavoriteRecipe


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

    @action(detail=False,
            permission_classes=[IsAuthenticated]
            )
    def message_shopping_cart(self, ingredients):
        shopping_list = 'Список продуктов:'
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}")
        file = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shoppingcart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        return self.message_shopping_cart(ingredients)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated]
            )
    def get_favorite(self, request):
        favorite = FavoriteRecipe.objects.filter(user=request.user)
        serializer = FavoriteSerializer(
            favorite,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True,
            methods=['POST'],
            permission_classes=[IsAuthenticated]
            )
    def favorite(self, request, pk):
        context = {'request': request}
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = FavoriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        get_object_or_404(
            FavoriteRecipe,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
