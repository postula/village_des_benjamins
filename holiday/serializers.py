from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import datetime
from django.core.exceptions import ObjectDoesNotExist

from holiday.models import (
    Holiday,
    HolidaySection,
    Registration,
    registration_statuses,
    Outing,
)


class OutingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "name",
            "description",
            "date",
            "departure_time",
            "arrival_time",
            "price",
            "transport",
        ]
        model = Outing


class HolidaySectionSerializer(serializers.ModelSerializer):
    section_id = serializers.ReadOnlyField(source="section.id")
    section_name = serializers.ReadOnlyField(source="section.name")
    capacities = serializers.SerializerMethodField()
    outings = OutingSerializer(many=True)

    def get_capacities(self, obj):
        holiday = obj.holiday
        capacities = {}
        current_date = holiday.start_date
        max_capacity = obj.capacity
        while current_date <= holiday.end_date:
            if current_date.weekday() < 5:
                already_booked = holiday.registration_set.filter(
                    dates__contains=[current_date]
                ).count()
            else:
                already_booked = max_capacity
            capacities[current_date.isoformat()] = max_capacity - already_booked
            current_date += datetime.timedelta(days=1)
        return capacities

    class Meta:
        model = HolidaySection
        fields = ["capacity", "section_id", "section_name", "capacities", "outings"]


class HolidaySerializer(serializers.ModelSerializer):
    sections = HolidaySectionSerializer(source="holidaysection_set", many=True)

    class Meta:
        model = Holiday
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "price",
            "registration_open",
            "description",
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

    class Meta:
        model = Registration
        fields = [
            "id",
            "holiday",
            "child",
            "status",
            "dates",
            "cost",
            "status_type",
            "section",
        ]
