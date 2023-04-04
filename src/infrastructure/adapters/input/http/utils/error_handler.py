import logging
from typing import Any, Optional, Dict

from fastapi import Request, FastAPI
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

from src.configuration import application_logger
from src.domain.utils.exceptions import ApplicationError


class ExceptionResponse:
    def __init__(self, message: str, data: Optional[Dict] = None):
        self.message = message
        self.data = data

    def serialize(self) -> Dict:
        return self.__dict__


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except (ApplicationError, Exception) as e:
            self.capture_exception(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if isinstance(e, ApplicationError):
                status_code = e.status_code
                exception_response = ExceptionResponse(message=e.message, data=e.data)
            else:
                exception_response = ExceptionResponse(
                    message="An uncontrolled error occurred. "
                            "Please try again later, or see the console if you are the administrator"
                )
            return JSONResponse(status_code=status_code, content=exception_response.serialize())

    @staticmethod
    def capture_exception(e: Exception) -> None:
        application_logger.log(logging.ERROR, f"Exception: {e}.")
