from tag.models import Tag
from .mixins import CreateListRetrieveViewSet
from .serializers import TagSerializer


class TagViewSet(CreateListRetrieveViewSet):  # id 1 нет
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
