from sqlalchemy import (
    Column, Text, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.adapters.output.repositories.entities import Base, Schemas
from src.infrastructure.adapters.output.repositories.entities.base_entity import BaseEntity
from src.infrastructure.adapters.output.repositories.entities.user_entity import UserEntity


class TokenEntity(Base, BaseEntity):
    __tablename__ = 'token'
    __table_args__ = {'schema': Schemas.auth.value}
    token = Column(Text, nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserEntity.id), primary_key=True)  # type: ignore
    user = relationship("UserEntity", backref="user_child")
