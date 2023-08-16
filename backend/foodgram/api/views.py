from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .mixins import CreateListViewSet, RetrieveListViewSet
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipeRetriveListSerializer,
    RecipeCreateUpdateSerializer,
    IngredientSerializer,
    TagSerializer, FavoriteSerializer,
    SubscribeSerializer, ShoppingCartSerializer)
from .filters import IngredientFilter, RecipeFilter
from users.models import Subscribe
from recipe.models import (Recipe,
                           Ingredient,
                           IngredientRecipe,
                           Tag,
                           ShoppingCartRecipe,
                           FavoriteRecipe)


User = get_user_model()


class CustomDjoserUserViewSet(UserViewSet):

    @action(detail=False,
            methods=['POST'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        users = User.objects.filter(followers__user=request.user)
        serializer = SubscribeSerializer(self.paginate_queryset(users),
                                         many=True,
                                         context={'request': request})
        return Response(serializer.data)

    @action(detail=True,
            methods=['POST'],
            permission_classes=[IsAuthenticated]
            )
    def subscribe(self, request, pk):
        context = {'request': request}
        author = get_object_or_404(User, id=pk)
        data = {
            'user': request.user.id,
            'author': author
        }
        serializer = SubscribeSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk):
        get_object_or_404(
            Subscribe,
            user=request.user.id,
            author=get_object_or_404(User, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeViewSet(CreateListViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        '=following__username',
        '=user__username'
    )

    def get_queryset(self):
        return self.request.user.is_subscribed.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
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
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shoppingcart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
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

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
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

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        get_object_or_404(
            ShoppingCartRecipe,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = []
    pagination_class = LimitOffsetPagination
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)


class TagViewSet(RetrieveListViewSet):  # id 1 нет
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCartRecipe.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = []
