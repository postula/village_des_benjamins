# from django.contrib.auth.models import User
from rest_framework import mixins, viewsets

from holiday.models import Holiday, Registration
from holiday.serializers import HolidaySerializer, RegistrationSerializer


class HolidayViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


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
