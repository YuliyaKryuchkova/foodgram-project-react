from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.api_recipe.serializers import RecipeSerializer
from subscribe.models import Subscribe


User = get_user_model()


class SubscribeListSerializer(serializers.ModelSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
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
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeSerializer(
            recipes,
            many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, object):
        if not self.context['request'].user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            author=object, user=self.context['request'].user).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = (
            'user',
            'author',

        )

    def to_representation(self, instance):
        return SubscribeListSerializer(
            instance.author,
            context={
                'request': self.context['request']
            }
        ).data

    def validate(self, attrs):
        author = attrs.get('author')
        user = attrs.get('user')
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError('Уже есть подписка')
        return attrs
