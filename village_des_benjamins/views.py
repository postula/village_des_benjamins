from django.db import connection, OperationalError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    try:
        connection.ensure_connection()
        return Response({"status": "ok", "database": "ok"})
    except OperationalError as exc:
        return Response(
            {"status": "error", "database": f"error: {exc}"},
            status=503,
        )
