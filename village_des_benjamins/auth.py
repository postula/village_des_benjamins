from logging import getLogger

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = getLogger(__name__)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["is_staff"] = user.is_staff
        # ...

        return token
