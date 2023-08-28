from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import ShoppingCartSerializer
from shoppingcartrecipe.models import ShoppingCartRecipe
from recipes.models import Recipe


@api_view(['POST', 'DELETE'])
def shopping_cart(request, pk):
    if request.method == 'POST':
        context = {'request': request}
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        get_object_or_404(
            ShoppingCartRecipe,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
