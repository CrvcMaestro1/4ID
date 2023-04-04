import uuid
from datetime import datetime, timedelta
from typing import Optional, Any, Dict

import jwt
from sqlalchemy import insert, delete
from sqlalchemy.orm import Session

from src import get_env_var
from src.domain.user.output.user_repository import UserRepository
from src.domain.user.user import Token, User
from src.infrastructure.adapters.output.repositories.database_engine_config import database_engine, DatabaseEnum
from src.infrastructure.adapters.output.repositories.entities import UserEntity, TokenEntity

JWT_SECRET_KEY = get_env_var('JWT_SECRET_KEY')


class UserRepositoryImpl(UserRepository):

    @database_engine(database_type=DatabaseEnum.master)
    def create_user(self, user: User, **kwargs: Optional[Any]) -> None:
        with Session(bind=kwargs.get('engine')) as session:
            create_user_query = (
                insert(UserEntity)
                .values({
                    "id": uuid.uuid1(), "username": user.username,
                    "password": UserEntity.generate_password(user.password)
                })
            )
            session.execute(create_user_query)
            session.commit()

    @database_engine(database_type=DatabaseEnum.master)
    def check_user(self, user: User, **kwargs: Optional[Any]) -> Optional[str]:
        with Session(bind=kwargs.get('engine')) as session:
            login_query = session.query(
                UserEntity.id, UserEntity.password
            ).where(UserEntity.username == user.username).first()
            if not login_query:
                return None
            if not UserEntity.verify_password(login_query.password, user.password):
                return None
            return str(login_query.id)

    @database_engine(database_type=DatabaseEnum.master)
    def generate_token(self, user_id: str, **kwargs: Optional[Any]) -> Optional[Token]:
        with Session(bind=kwargs.get('engine')) as session:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=15), 'iat': datetime.utcnow(), 'sub': user_id
            }
            generated_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

            remove_old_token = (
                delete(TokenEntity)
                .where(TokenEntity.user_id == user_id)
            )
            session.execute(remove_old_token)

            set_user_token = (
                insert(TokenEntity)
                .values({"token": generated_token, "user_id": user_id})
            )
            session.execute(set_user_token)

            session.commit()

            return Token(token=generated_token)

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @database_engine(database_type=DatabaseEnum.master)
    def remove_token(self, token: str, decoded_token: Dict, **kwargs: Optional[Any]) -> None:
        with Session(bind=kwargs.get('engine')) as session:
            user_id = decoded_token.get('sub')
            remove_token = (
                delete(TokenEntity)
                .where(TokenEntity.token == token, TokenEntity.user_id == user_id)
            )
            session.execute(remove_token)
            session.commit()
