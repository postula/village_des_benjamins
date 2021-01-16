# from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from parent_messages.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            "id",
            "name",
            "email",
            "message"
        ]
        model = Message
