# from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from members.models import User, Child
from members.permissions import IsOwnerOrReadOnly
from members.serializers import UserSerializer, ChildSerializer, TeamSerializer
from logging import getLogger

logger = getLogger(__name__)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ["retrieve", "list"]:
            qs = qs.filter(parent=self.request.user)
        return qs


class TeamViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = TeamSerializer
    queryset = User.objects.filter(is_staff=True, visible_on_site=True).order_by(
        "role__order", "first_name"
    )
