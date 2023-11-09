from fastapi import APIRouter

from app.rest_api.api.position import position_router
from app.rest_api.api.province import province_router
from app.rest_api.api.user import user_router
from app.rest_api.api.banner import banner_router

rest_router = APIRouter()
rest_router.include_router(user_router)
rest_router.include_router(province_router)
rest_router.include_router(position_router)
rest_router.include_router(banner_router)
