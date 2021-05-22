# from django.contrib.auth.models import User
import datetime

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from holiday.models import Holiday, Registration
from holiday.serializers import HolidaySerializer, RegistrationSerializer


class HolidayViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def get_capacity(self, request, pk=None):
        holiday = self.get_object()
        sections = {}
        for section in holiday.holidaysection_set.all():
            capacities = {}
            current_date = holiday.start_date
            max_capacity = section.capacity
            while current_date <= holiday.end_date:
                if current_date.weekday() < 5:
                    already_booked = holiday.registration_set.filter(
                        dates__contains=[current_date]
                    ).count()
                else:
                    already_booked = max_capacity
                capacities[current_date.isoformat()] = max_capacity - already_booked
                current_date += datetime.timedelta(days=1)
            sections[section.section_id] = capacities
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
