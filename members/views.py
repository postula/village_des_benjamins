# from django.contrib.auth.models import User
from rest_framework import mixins, viewsets

from members.models import User, Child
from members.permissions import IsOwnerOrReadOnly, IsParent
from members.serializers import UserSerializer, ChildSerializer


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
