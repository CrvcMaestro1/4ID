import uuid

import bcrypt
from sqlalchemy import (
    Column, String
)
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.adapters.output.repositories.entities import Base, Schemas
from src.infrastructure.adapters.output.repositories.entities.base_entity import BaseEntity


class UserEntity(Base, BaseEntity):
    __tablename__ = 'user'
    __table_args__ = {'schema': Schemas.auth.value}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1, unique=True)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    @staticmethod
    def verify_password(password: str, password_in: str) -> bool:
        hashed_password = bcrypt.hashpw(password_in.encode('utf-8'), password.encode('utf-8')).decode('utf-8')
        return password == hashed_password

    @staticmethod
    def generate_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
