# from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from members.models import User, Child
from members.permissions import IsOwnerOrReadOnly, IsParent
from members.serializers import UserSerializer, ChildSerializer, TeamSerializer


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
        return super().get_permissions()


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            self.permission_classes = [IsParent]
        return super().get_permissions()


class TeamViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = TeamSerializer
    queryset = User.objects.filter(is_staff=True, visible_on_site=True).order_by("role__order")
