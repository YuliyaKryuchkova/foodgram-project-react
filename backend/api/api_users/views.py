from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.api_subscribe.serializers import SubscribeSerializer
from .pagination import LimitPageNumberPagination

User = get_user_model()


class CustomDjoserUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        users = User.objects.filter(followers__user=request.user)
        serializer = SubscribeSerializer(self.paginate_queryset(users),
                                         many=True,
                                         context={'request': request})
        return Response(serializer.data)
