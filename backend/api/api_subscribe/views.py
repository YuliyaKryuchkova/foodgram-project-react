# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.generics import get_object_or_404
# from rest_framework.response import Response
#
# from subscribe.models import Subscribe
# from .serializers import SubscribeSerializer
#
# User = get_user_model()
#
#
# @api_view(['POST', 'DELETE'])
# def subscribe(request, id):
#     if request.method == 'POST':
#         context = {'request': request}
#         author = get_object_or_404(User, id=id)
#         data = {
#             'user': request.user.id,
#             'author': author.id
#         }
#         serializer = SubscribeSerializer(data=data, context=context)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         get_object_or_404(
#             Subscribe,
#             user=request.user.id,
#             author=get_object_or_404(User, id=id)
#         ).delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
