# from django.contrib.auth.hashers import make_password
from rest_framework import serializers
# import datetime
# from django.core.exceptions import ObjectDoesNotExist

from site_content.models import (
    Content,
    SiteSection,
    News,
)


class NewsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d/%m/%y", read_only=True)

    class Meta:
        fields = [
            "id",
            "date",
            "description"
        ]
        model = News


class SiteSectionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            "id",
            "name",
            "key",
            "description",
            "order",
            "photo",
            "layout",
            "background",
        ]
        model = SiteSection


class ContentSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(slug_field="key", read_only=True)

    class Meta:
        fields = [
            "id",
            "name",
            "section",
            "description",
            "icon",
            "order",
            "show_more_button",
            "show_more_content",
        ]
        model = Content


