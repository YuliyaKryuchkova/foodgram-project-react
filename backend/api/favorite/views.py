from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import FavoriteSerializer
from favoriterecipe.models import FavoriteRecipe
from recipes.models import Recipe


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite(request, pk=None):
    if request.method == 'POST':
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
    elif request.method == 'DELETE':
        get_object_or_404(
            FavoriteRecipe,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
