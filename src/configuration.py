import logging
import socket
from typing import Dict, Any
from logging.config import dictConfig  # noqa
import inject
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.domain.user.input.user_service import UserService
from src.domain.user.output.user_repository import UserRepository
from src.domain.user.user_service_impl import UserServiceImpl
from src.infrastructure.adapters.output.repositories.user_repository_impl import UserRepositoryImpl


def configure_inject() -> None:
    def config_repositories(binder: inject.Binder) -> None:
        binder.bind_to_provider(UserRepository, UserRepositoryImpl)

    def config_services(binder: inject.Binder) -> None:
        binder.bind_to_provider(UserService, UserServiceImpl)

    def config(binder: inject.Binder) -> None:
        config_repositories(binder)
        config_services(binder)

    inject.configure(config)


def configure_validation_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Any, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder({"errors": exc.errors()})
        )


def configure_logging() -> Dict:
    hostname = socket.gethostname()
    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'datefmt': '%Y-%m-%d %H:%M:%S',
                '()': 'colorlog.ColoredFormatter',
                'format': f'{hostname}:  %(log_color)s%(levelname)s %(message)s',
                'log_colors': {
                    'DEBUG': 'green',
                    'INFO': 'cyan',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            '4id-challenge-service': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            }
        }
    }
    return logging


logging.config.dictConfig(configure_logging())
application_logger = logging.getLogger("4id-challenge-service")
