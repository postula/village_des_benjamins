from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from members.models import User, Child


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def validate_password(self, value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "is_staff",
            "email",
            "password",
            "photo",
        ]


class CurrentUserDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current user.
    """

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user


class ChildSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(slug_field="name", read_only=True)
    parent = serializers.HiddenField(default=serializers.CurrentUserDefault())

    holidays_booked = serializers.SerializerMethodField()

    def get_holidays_booked(self, obj):
        return obj.registrations.values_list("holiday__id", flat=True)

    class Meta:
        model = Child
        fields = [
            "id",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "section",
            "parent",
            "holidays_booked",
        ]
