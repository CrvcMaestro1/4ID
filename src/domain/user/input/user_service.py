from abc import (
    ABCMeta, abstractmethod,
)

from src.domain.user.user import User, Token


class UserService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def sign_up(self, user: User) -> None:
        pass

    @abstractmethod
    def sign_in(self, user: User) -> Token:
        pass

    @abstractmethod
    def sign_out(self, token: Token) -> None:
        pass
