from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.api_tag.serializers import TagSerializer
from api.api_users.serializers import CustomUserSerializer
from ingredient.models import Ingredient
from recipes.models import IngredientRecipe, Recipe
from .api_favorite.serializers import FavoriteSerializer
from favoriterecipe.models import FavoriteRecipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeCreateIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class RecipeRetriveListSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField()
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'favorite'
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )

    def get_is_favorited(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.is_favorited.filter(
            user=self.context['request'].user
        ).exists()

    def get_favorite(self, obj):
        favorite = FavoriteRecipe.objects.filter(recipe=obj)
        return FavoriteSerializer(favorite, many=True).data

    def get_is_in_shopping_cart(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.shoppingcart.filter(user=self.context['request'].user)

    def get_ingredients(self, obj):
        return RecipeCreateIngredientSerializer(
            obj.ingredient_recipes,
            many=True
        ).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_favorited'] = self.get_is_favorited(instance)
        return representation


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = RecipeCreateIngredientSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_something(self, obj, model):
        if not self.context['request'].user.is_authenticated:
            return False
        return model.objects.filter(
            recipe=obj, user=self.context['request'].user).exists()

    def create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe, ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        obj = Recipe.objects.create(
            author=author,
            **validated_data
        )
        obj.tags.set(tags)
        self.create_ingredients(obj, ingredients)
        return obj

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeRetriveListSerializer(
            instance,
            context={
                'request': self.context['request']
            }
        ).data

    def validate_ingredients(self, values):
        list_ingredient_id = []
        for value in values:
            id = value.get('ingredient').id
            if id not in list_ingredient_id:
                list_ingredient_id.append(id)
                continue
            raise serializers.ValidationError(
                'Ингридиент уже в списке'
            )
        return values
