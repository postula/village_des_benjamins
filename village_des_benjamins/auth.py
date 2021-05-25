from logging import getLogger

from django.utils.encoding import smart_text
from jwt import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext_lazy as _

logger = getLogger(__name__)


def get_jwt_value(request):
    auth = request.headers.get("Authorizationfb", None)
    if auth is not None:
        auth = auth.split()
    auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

    if not auth:
        if api_settings.JWT_AUTH_COOKIE:
            return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
        return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = _('Invalid Authorization header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _('Invalid Authorization header. Credentials string '
                'should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)

    return auth[1]


class JSONWebTokenAuthenticationNewHeader(JSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        token = super().get_jwt_value(request)
        if not token:
            token = get_jwt_value(request)
        return token
