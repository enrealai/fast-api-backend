from fastapi import APIRouter, Depends, Query

from app.controllers import AuthController, UserController
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from app.container import Container

def create_user_router(container: Container) -> APIRouter:
    user_router = APIRouter()

    @user_router.post("/", status_code=201)
    async def register_user(
        register_user_request: RegisterUserRequest,
        auth_controller: AuthController = Depends(container.get_auth_controller),
    ) -> UserResponse:
        return await auth_controller.register(
            email=register_user_request.email,
            password=register_user_request.password,
            username=register_user_request.username,
        )


    @user_router.post("/login")
    async def login_user(
        login_user_request: LoginUserRequest,
        auth_controller: AuthController = Depends(container.get_auth_controller),
    ) -> Token:
        return await auth_controller.login(
            email=login_user_request.email, password=login_user_request.password
        )


    @user_router.get("/user")
    async def get_user(
        username: str = Query(..., description="Username of the user"),
        user_controller: UserController = Depends(container.get_user_controller),
    ) -> UserResponse:
        return await user_controller.get_by_username(
            username = username
        )


    return user_router
