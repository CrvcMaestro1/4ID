import enum
import random
from typing import List, Callable, TypeVar, Any, cast

from sqlalchemy import create_engine

from src import get_env_var


class DatabaseEnum(enum.Enum):
    master = "master"
    replica = "replica"


def get_databases_from_environment() -> List[str]:
    data_base_list = list()
    for db_name in get_env_var("DATABASES_REPLICA_POOL").split(","):
        db_name = db_name.strip()
        data_base_list.append(db_name)
    return data_base_list


FuncT = TypeVar("FuncT", bound=Callable[..., Any])


def database_engine(database_type: DatabaseEnum) -> Callable[[FuncT], Callable[[FuncT], FuncT]]:
    def decorator(function: FuncT) -> Callable[[FuncT], FuncT]:
        def wrapper(*args: Any, **kwargs: Any) -> FuncT:
            db_name = "DATABASE_APPLICATION"
            if database_type == DatabaseEnum.replica:
                database_list = get_databases_from_environment()
                db_name = random.choice(database_list)
            database_uri = get_env_var(db_name)
            engine = create_engine(database_uri)
            kwargs['engine'] = engine.connect()
            return function(*args, **kwargs)
        return cast(FuncT, wrapper)

    return decorator
