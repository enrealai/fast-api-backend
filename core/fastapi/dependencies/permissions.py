from http import HTTPStatus

from fastapi import Depends, Request

from app.controllers.userController import UserController
from core.exceptions import CustomException
from app.container import Container
from core.security.access_control import (
    AccessControl,
    Authenticated,
    Everyone,
    RolePrincipal,
    UserPrincipal,
)


class InsufficientPermissionsException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = "Insufficient permissions"


async def get_user_principals(
    request: Request,
    user_controller: UserController = Depends(Container().get_user_controller),
) -> list:
    user_id = request.user.id
    principals = [Everyone]

    if not user_id:
        return principals

    user = await user_controller.get_by(field="uuid", value=user_id)

    principals.append(Authenticated)
    principals.append(UserPrincipal(user.id))

    if user.is_admin:
        principals.append(RolePrincipal("admin"))

    return principals


Permissions = AccessControl(
    principals_getter=get_user_principals,
    permission_exception=InsufficientPermissionsException,
)
