from fastapi import APIRouter

from app.rest_api.api.user import user_router

rest_router = APIRouter()
rest_router.include_router(user_router)
