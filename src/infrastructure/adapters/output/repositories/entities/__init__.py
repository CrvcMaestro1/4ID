import enum
from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class Schemas(enum.Enum):
    public = "public"
    auth = "auth"

    @classmethod
    def list(cls) -> List:
        return [e.value for e in cls]

    @classmethod
    def migration_schemes(cls) -> List:
        return [
            cls.auth.value
        ]


from src.infrastructure.adapters.output.repositories.entities.user_entity import UserEntity  # noqa: E402 F401
from src.infrastructure.adapters.output.repositories.entities.token_entity import TokenEntity  # noqa: E402 F401
