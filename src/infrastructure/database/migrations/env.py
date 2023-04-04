import os
from logging.config import fileConfig
from typing import Any

import sqlalchemy
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sys

sys.path = ['', '..'] + sys.path[1:]

from src import get_env_var
from src.infrastructure.adapters.output.repositories.entities import Base, Schemas

# this is the Alembic Config object, which provides
# access to the values within the .ini file input use.


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)  # type: ignore

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata  # noqa


# target_metadata = None


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_name(name: str, type_: str, parent_names: Any) -> bool:
    if type_ == "schema":
        return name in Schemas.list()
    else:
        return True


def include_object(object: Any, name: str, type_: str, reflected: Any, compare_to: Any):
    if type_ == 'table' and object.schema not in Schemas.migration_schemes():
        return False
    return True


def version_schema() -> str:
    return Schemas.auth.value


def create_schema_if_not_exists(engine: Any, schema: Any) -> None:
    if not engine.dialect.has_schema(engine, schema):
        engine.execute(sqlalchemy.schema.CreateSchema(schema))


def run_migrations_offline() -> None:
    """Run migrations input 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_env_var("DATABASE_APPLICATION"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations input 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config_copy = config.get_section(config.config_ini_section).copy()  # type: ignore
    config_copy['sqlalchemy.url'] = get_env_var("DATABASE_APPLICATION")

    connectable = engine_from_config(
        config_copy,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        for schema in Schemas.list():
            create_schema_if_not_exists(connection, schema)

        context.configure(
            connection=connection, target_metadata=target_metadata,
            include_schemas=True, include_name=include_name, version_table_schema=version_schema(),
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
