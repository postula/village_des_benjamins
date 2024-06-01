from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import datetime
from django.core.exceptions import ObjectDoesNotExist

from holiday.models import (
    Holiday,
    HolidaySection,
    Registration,
    registration_statuses,
    Outing, SectionProgram,
)
from members.models import User


class AnimateurSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "first_name",
            "last_name"
        ]
        model = User


class SectionProgramSerializer(serializers.ModelSerializer):
    animateur = AnimateurSerializer(many=True)

    class Meta:
        fields = [
            "id",
            "description",
            "start_date",
            "end_date",
            "animateur",
            "theme",
            "bricolage",
            "food",
            "game",
            "other"
        ]
        model = SectionProgram


class OutingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "departure_time",
            "arrival_time",
            "price",
            "transport",
        ]
        model = Outing


class HolidaySectionSerializer(serializers.ModelSerializer):
    section_id = serializers.ReadOnlyField(source="section.id")
    section_name = serializers.ReadOnlyField(source="section.name")
    section_animateurs = AnimateurSerializer(many=True, source="section.educators", read_only=True)
    outings = serializers.SerializerMethodField('get_outings_list')
    activities = serializers.SerializerMethodField('get_activities_list')

    def get_outings_list(self, instance):
        outings = instance.outings.order_by(
            "start_date"
        )
        return OutingSerializer(
            outings,
            many=True,
            context=self.context
        ).data

    def get_activities_list(self, instance):
        activities = instance.activities.order_by(
            "start_date",
        ).prefetch_related('animateur')
        return SectionProgramSerializer(
            activities,
            many=True,
            context=self.context
        ).data

    class Meta:
        model = HolidaySection
        fields = ["activities", "section_id", "section_name", "section_animateurs", "outings", "description"]


class HolidaySerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField('get_sections_list')

    def get_sections_list(self, instance):
        hs = HolidaySection.objects.filter(
            holiday_id=instance.id
        ).order_by(
            "section__order"
        ).prefetch_related(
            "outings",
            "activities",
            "activities__animateur"
        )
        return HolidaySectionSerializer(
            hs,
            many=True,
            context=self.context
        ).data

    class Meta:
        model = Holiday
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "price",
            "blacklisted_dates",
            "registration_open",
            "description",
            "book_by_day",
            "sections",
        ]


class RegistrationSerializer(serializers.ModelSerializer):

    status_type = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=registration_statuses, read_only=True)

    def get_status_type(self, obj):
        if obj.status == "pending":
            return "warning"
        elif obj.status == "paid":
            return "success"
        elif obj.status == "cancelled":
            return "danger"

    def create(self, validated_data):
        holiday_registration_open = validated_data.get("registration_open")
        request = self.context.get("request")
        is_staff = False
        if request and hasattr(request, "user"):
            user = request.user
            is_staff = user.is_staff
        if not holiday_registration_open and not is_staff:
            raise serializers.ValidationError("Cannot create registration on close registration")
        return super().create(validated_data)

    class Meta:
        model = Registration
        fields = [
            "id",
            "holiday",
            "child",
            "status",
            "dates",
            "notes",
            "cost",
            "status_type",
            "section",
        ]
