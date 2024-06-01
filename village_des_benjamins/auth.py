from logging import getLogger

from django.utils.encoding import smart_text
from jwt import exceptions
from rest_framework_jwt.utils import jwt_payload_handler as base_jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext_lazy as _

logger = getLogger(__name__)


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    payload = base_jwt_payload_handler(user)
    # Add is_staff to it
    payload['is_staff'] = user.is_staff
    return payload


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
