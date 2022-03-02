# from django.contrib.auth.models import User
import datetime

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from holiday.models import Holiday, Registration
from holiday.serializers import HolidaySerializer, RegistrationSerializer
from members.models import Child


class HolidayViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    # permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset().order_by("-start_date")
        if self.action in ["retrieve", "list"]:
            if self.request.user.is_staff:
                return qs
            return qs.filter(registration_open=True)
        return qs

    @action(detail=True, methods=['get'])
    def get_section_for_child(self, request, pk=None):
        holiday = self.get_object()
        child_id = request.query_params.get("child_id")
        child = Child.objects.get_date_queryset(holiday.start_date).get(id=child_id)
        return Response({"section_name": child.section})

    @action(detail=True, methods=['get'])
    def get_capacity(self, request, pk=None):
        holiday = self.get_object()
        dates = []
        current_date = holiday.start_date
        while current_date < holiday.end_date:
            if current_date.weekday() > 4:
                # weekend
                current_date += datetime.timedelta(days=1)
                continue
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
        dates.append(current_date)
        sections = {}
        for holiday_section in holiday.holiday_sections.all():
            sections[holiday_section.section.id] = {}
            for date in dates:
                sections[holiday_section.section.id][date.isoformat()] = holiday_section.capacity - Registration.objects.filter(section=holiday_section.section,
                                                                           dates__contains=[date]).count()
        return Response(sections)


class RegistrationViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Registration.objects.all()
    #  queryset = Registration.objects.filter(holiday__registration_open=True)
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ["retrieve", "list"]:
            qs = qs.filter(child__parent=self.request.user)
        return qs
