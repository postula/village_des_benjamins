from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from parent_messages.models import Message
from parent_messages.serializers import MessageSerializer


class MessageViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowAny]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
