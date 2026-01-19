# from django.contrib.auth.hashers import make_password
from rest_framework import serializers

# import datetime
# from django.core.exceptions import ObjectDoesNotExist

from site_content.models import (
    Content,
    SiteSection,
    News,
    ContentPlanning,
)


class NewsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d/%m/%y", read_only=True)

    class Meta:
        fields = ["id", "date", "description"]
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


class ContentPlanningSerializer(serializers.ModelSerializer):
    """Nested serializer for planning entries."""

    date = serializers.DateField(format="%d/%m/%Y")
    educator_name = serializers.SerializerMethodField()
    section_name = serializers.CharField(source="get_section_display", read_only=True)

    def get_educator_name(self, obj):
        return str(obj.educator) if obj.educator else None

    class Meta:
        model = ContentPlanning
        fields = ["id", "date", "educator_name", "section_name", "description"]


class ContentSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(slug_field="key", read_only=True)
    planning_entries = ContentPlanningSerializer(many=True, read_only=True)

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
            "planning_entries",
        ]
        model = Content
