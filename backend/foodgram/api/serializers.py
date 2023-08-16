from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from users.models import User, Subscribe
from recipe.models import (
    Recipe,
    Ingredient,
    ShoppingCartRecipe,
    Tag,
    IngredientRecipe,
    FavoriteRecipe)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = (
            obj.user.recipe.all()[:int(limit)] if limit
            else obj.user.recipe.all())
        return SubscribeRecipeSerializer(
            recipes,
            many=True).data

    def get_recipes_count(self, obj):
        return obj.user.recipe.count()

    def get_is_subscribed(self, object):
        if not self.context['request'].user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            author=object, user=self.context['request'].user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username']
        )
        user.set_password(data['password'])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, object):
        if not self.context['request'].user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            author=object, user=self.context['request'].user).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
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

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )

    def get_is_favorited(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.is_favorited.filter(user=self.context['request'].user)

    def get_is_in_shopping_cart(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.shoppingcart.filter(user=self.context['request'].user)

    def get_ingredients(self, obj):
        return RecipeCreateIngredientSerializer(
            obj.ingredient_recipes,
            many=True
        ).data


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = RecipeCreateIngredientSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(required=False)

    def get_something(self, obj, model):
        if not self.context['request'].user.is_authenticated:
            return False
        return model.objects.filter(
            recipe=obj, user=self.context['request'].user).exists()

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        obj = Recipe.objects.create(
            author=author,
            **validated_data
        )
        obj.save()

        obj.tags.set(tags)

        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=obj, ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ).save()

        return obj

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.tags.set(tags)
        instance.image = validated_data.get('image', instance.image)

        instance.ingredients.clear()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=instance, ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ).save()

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields['tags'] = TagSerializer(many=True)

        representation = super().to_representation(instance)

        representation['ingredients'] = RecipeIngredientSerializer(
            IngredientRecipe.objects.filter(
                recipe=instance).all(), many=True).data

        representation['is_favorite'] = self.get_something(
            instance,
            FavoriteRecipe
        )

        representation['is_in_shopping_cart'] = self.get_something(
            instance,
            ShoppingCartRecipe
        )

        return representation

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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe',)

    def is_favorited_validate(self, data):
        user = data['user']
        if user.is_favorited.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт в избранном.'
            )
        return data

    def to_representation(self, instance):
        return RecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


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
