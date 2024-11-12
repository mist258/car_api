from typing import Type

from django.contrib.auth import get_user_model

from rest_framework.generics import get_object_or_404

from core.enums.action_token_enum import ActionTokenEnum
from core.exceptions.jwt_exception import JwtException
from rest_framework_simplejwt.tokens import BlacklistMixin, Token

UserModel = get_user_model()

ActionTokenClassType = Type[BlacklistMixin | Token]


class ActionToken(BlacklistMixin, Token):
    pass


class ActivateToken(ActionToken):
    token_type = ActionTokenEnum.ACTIVATE.token_type
    lifetime = ActionTokenEnum.ACTIVATE.lifetime


class RecoveryToken(ActionToken):
    token_type = ActionTokenEnum.RECOVERY.token_type
    lifetime = ActionTokenEnum.RECOVERY.lifetime


class SocketToken(ActionToken):
    token_type = ActionTokenEnum.SOCKET.token_type
    lifetime = ActionTokenEnum.SOCKET.lifetime


class JWTService:

    @staticmethod
    def create_token(user, token_class:ActionTokenClassType):
        return token_class.for_user(user)

    @staticmethod
    def verify_token(token, token_class:ActionTokenClassType):
        try:
            token_result = token_class(token)
            token_result.check_blacklist()
        except Exception :
            raise JwtException

        token_result.blacklist()
        user_id = token_result.payload.get('user_id')
        return get_object_or_404(UserModel, pk=user_id)
