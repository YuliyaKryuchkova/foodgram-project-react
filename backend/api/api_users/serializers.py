from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from subscribe.models import Subscribe


User = get_user_model()


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
        # extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('username Me не разрешен')
        return value


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
        user = self.context['request'].user
        return user.is_authenticated and Subscribe.objects.filter(
            author=object, user=self.context['request'].user).exists()
