# from django.contrib.auth.hashers import make_password
from rest_framework import serializers
# import datetime
# from django.core.exceptions import ObjectDoesNotExist

from site_content.models import (
    Content,
)


class ContentSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        fields = [
            "id",
            "name",
            "section",
            "description",
            "icon",
        ]
        model = Content


