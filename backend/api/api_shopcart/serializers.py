from rest_framework import serializers

from api.api_recipe.serializers import RecipeSerializer
from shoppingcartrecipe.models import ShoppingCartRecipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartRecipe
        fields = ('user',
                  'recipe',
                  )

    def shoppingcart_validate(self, data):
        user = data['user']
        if user.shoppingcart.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт в корзине.'
            )
        return data

    def to_representation(self, instance):
        return RecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
