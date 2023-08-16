from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipe.models import Ingredient, Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.NumberFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_shoppingcart_validate'
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def filter_is_favorited_validate(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(is_favorited__user=self.request.user)
        return queryset

    def filter_shoppingcart_validate(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shoppingcart__user=self.request.user)
        return
