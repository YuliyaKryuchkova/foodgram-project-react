from tag.models import Tag
from .mixins import ListRetrieveViewSet
from .serializers import TagSerializer


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
