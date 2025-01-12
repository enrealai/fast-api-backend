from typing import Callable

from fastapi import APIRouter, Depends

from app.controllers import AuthController, UserController
from app.models.user import UserPermission
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest, UserInfoRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.permissions import Permissions

user_router = APIRouter()


@user_router.get("/", dependencies=[Depends(AuthenticationRequired)])
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
    assert_access: Callable = Depends(Permissions(UserPermission.READ)),
) -> list[UserResponse]:
    users = await user_controller.get_all()

    assert_access(resource=users)
    return users


@user_router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )


@user_router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )


@user_router.get("/user", dependencies=[Depends(AuthenticationRequired)])
async def get_users(
    user_info_request: UserInfoRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    return await user_controller.get_by_username(
        username = user_info_request.username
    )