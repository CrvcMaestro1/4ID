from typing import Dict

from fastapi import APIRouter
from starlette import status


def health_router() -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get('/healthz', response_model=Dict, status_code=status.HTTP_200_OK)
    async def health_check() -> Dict:
        return {"message": "ok"}

    return router


def health_check_root() -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get('/', response_model=Dict, status_code=status.HTTP_200_OK)
    async def health_check() -> Dict:
        return {"message": "ok"}

    return router
