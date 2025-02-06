from typing import Optional, Tuple

from jose import JWTError
from fastapi import Request
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)

from core.security.jwt import JWTHandler

class AuthBackend(AuthenticationBackend):
    def __init__(self, require_user_id_match: bool = True):
        self.require_user_id_match = require_user_id_match

    async def authenticate(
        self, request: Request
    ) -> Tuple[bool, Optional[str]]:
        authorization: str = request.headers.get("Authorization")
        user_id: str = request.headers.get("user_id")
        if not authorization or not user_id:
            return False, None

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, None
        except ValueError:
            return False, None

        if not token:
            return False, None
        try:
            tokenPayload = JWTHandler.decode(token)
            if self.require_user_id_match and user_id != tokenPayload.get("user_id"):
                return False, None
        except JWTError:
            return False, None

        return True, user_id

class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
