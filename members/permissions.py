from rest_framework import permissions
from logging import getLogger

logger = getLogger(__name__)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return request.user.is_superuser or request.user == obj
        return False
