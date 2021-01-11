from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from site_content.models import Content
from site_content.serializers import ContentSerializer


class ContentViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowAny]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
