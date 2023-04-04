import inject
from fastapi import APIRouter
from starlette import status

from src.domain.user.input.user_service import UserService
from src.domain.user.user import Token, User


@inject.autoparams()
def user_router(user_service: UserService) -> APIRouter:
    router = APIRouter(tags=["User"])

    @router.post(
        '/sign-up', status_code=status.HTTP_204_NO_CONTENT, summary="SignOut API endpoint",
        description="The input parameters are user and password for the SignOut API. For example purposes"
    )
    async def sign_up(user: User) -> None:
        return user_service.sign_up(user)

    @router.post(
        '/sign-in', response_model=Token, status_code=status.HTTP_200_OK, summary="SignIn API endpoint",
        description="The input parameters are user and password for the SignIn API"
    )
    async def sign_in(user: User) -> Token:
        return user_service.sign_in(user)

    @router.delete(
        '/sign-out', status_code=status.HTTP_204_NO_CONTENT, summary="SignOut API endpoint",
        description="The input parameters are user for the SignOut API"
    )
    async def sign_out(token: Token) -> None:
        user_service.sign_out(token)

    return router
