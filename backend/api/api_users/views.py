from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.generics import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
#
# from api.api_subscribe.serializers import SubscribeSerializer
from .pagination import LimitPageNumberPagination
# from subscribe.models import Subscribe

User = get_user_model()


class CustomDjoserUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    #
    # @action(detail=False,
    #         methods=['GET'],
    #         permission_classes=[IsAuthenticated])
    # def subscriptions(self, request):
    #     users = Subscribe.objects.filter(followers__user=request.user)
    #     serializer = SubscribeSerializer(self.paginate_queryset(users),
    #                                      many=True,
    #                                      context={'request': request})
    #     return Response(serializer.data)
    #
    # @action(detail=True,
    #         methods=['POST'],
    #         permission_classes=[IsAuthenticated]
    #         )
    # def subscribe(self, request, id):
    #     context = {'request': request}
    #     author = get_object_or_404(User, id=id)
    #     data = {
    #         'user': request.user.id,
    #         'author': author.id
    #     }
    #     serializer = SubscribeSerializer(data=data, context=context)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # @subscribe.mapping.delete
    # def delete_subscribe(self, request, id):
    #     get_object_or_404(
    #         Subscribe,
    #         user=request.user.id,
    #         author=get_object_or_404(User, id=id)
    #     ).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
