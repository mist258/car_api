from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def error_handler(exc: Exception, context: dict) -> Response:
    handlers = {
        "JwtException": _jwt_validation_error_handler
    }

    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context)

    return response

def _jwt_validation_error_handler(exc: Exception, context:dict) -> Response:
    return Response({'detail' : 'Tolen is invalid or expired'}, status.HTTP_400_BAD_REQUEST)