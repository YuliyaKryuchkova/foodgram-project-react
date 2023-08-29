# from rest_framework import serializers
#
# from api.api_recipe.serializers import (
#     RecipeSerializer,
#     RecipeRetriveListSerializer
# )
# from favoriterecipe.models import FavoriteRecipe
#
#
# class FavoriteSerializer(serializers.ModelSerializer):
#     recipe = RecipeRetriveListSerializer()
#
#     class Meta:
#         model = FavoriteRecipe
#         fields = (
#             'user',
#             'recipe',
#         )
#
#     def validate(self, data):
#         user = data['user']
#         if user.is_favorited.filter(recipe=data['recipe']).exists():
#             raise serializers.ValidationError(
#                 'Рецепт в избранном.'
#             )
#         return data
#
#     def to_representation(self, instance):
#         return RecipeSerializer(
#             instance.recipe,
#             context={'request': self.context.get('request')}
#         ).data
