from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.configuration import (
    configure_inject, configure_validation_handler, configure_logging
)
from src.infrastructure.adapters.input.http.utils.error_handler import ErrorHandler
from src.infrastructure.adapters.input.http.v1 import (
    user_controller, health_controller
)


def create_application() -> FastAPI:
    application = FastAPI(
        title='4ID Authentication',
        description='4ID Authentication Service',
        openapi_url="/openapi.json",
        docs_url="/docs"
    )
    configure_inject()
    configure_validation_handler(application)
    application.add_middleware(ErrorHandler)
    dictConfig(configure_logging())
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    application.include_router(
        router=user_controller.user_router()
    )
    application.include_router(
        router=health_controller.health_check_root()
    )
    return application


app = create_application()
