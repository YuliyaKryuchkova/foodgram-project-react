from tag.models import Tag
from .mixins import CreateListRetrieveViewSet
from .serializers import TagSerializer


class TagViewSet(CreateListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
