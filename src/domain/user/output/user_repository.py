from abc import (
    ABCMeta, abstractmethod
)
from typing import Optional, Dict

from src.domain.user.user import User, Token


class UserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create_user(self, user: User) -> None:
        pass

    @abstractmethod
    def check_user(self, user: User) -> Optional[str]:
        pass

    @abstractmethod
    def generate_token(self, user_id: str) -> Optional[Token]:
        pass

    @abstractmethod
    def remove_token(self,  token: str, decoded_token: Dict) -> None:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Optional[Dict]:
        pass
