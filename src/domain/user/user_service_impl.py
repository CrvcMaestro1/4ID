import inject

from src.domain.user.input.user_service import UserService
from src.domain.user.output.user_repository import UserRepository
from src.domain.user.user import Token, User
from src.domain.utils.exceptions import ApplicationError


class UserServiceImpl(UserService):

    @inject.autoparams()
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def sign_up(self, user: User) -> None:
        self.user_repository.create_user(user)

    def sign_in(self, user: User) -> Token:
        user_id = self.user_repository.check_user(user)
        if not user_id:
            raise ApplicationError(403, "Wrong credentials", data={"user": user.username})
        token = self.user_repository.generate_token(user_id)
        if not token:
            raise ApplicationError(403, "A problem occurred generating the token", data={"user_id": user_id})
        return token

    def sign_out(self, token: Token) -> None:
        decoded_token = self.user_repository.decode_token(token.token)
        if not decoded_token:
            raise ApplicationError(403, "A problem occurred decoding the token", data={"token": token.token})
        self.user_repository.remove_token(token.token, decoded_token)
