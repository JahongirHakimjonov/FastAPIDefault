from fastapi.routing import APIRouter

from api.api_v1 import dummy

api_router = APIRouter()
api_router.include_router(dummy.router)
