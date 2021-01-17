from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from site_content.models import Content, SiteSection, News
from site_content.serializers import ContentSerializer, SiteSectionSerializer, NewsSerializer


class NewsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowAny]
    queryset = News.objects.all().order_by("-date")
    serializer_class = NewsSerializer


class SiteSectionViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowAny]
    queryset = SiteSection.objects.all()
    serializer_class = SiteSectionSerializer


class ContentViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowAny]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
