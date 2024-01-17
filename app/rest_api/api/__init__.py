from fastapi import APIRouter

from app.rest_api.api.position import position_router
from app.rest_api.api.province import province_router
from app.rest_api.api.user import user_router

# Match
from app.rest_api.api.match.match import match_router

# Guest
from app.rest_api.api.guest.guest import guest_router

# Notfication
from app.rest_api.api.notification.faq import faq_router

# Etc(banner...)
from app.rest_api.api.banner import banner_router
from app.rest_api.api.club import club_router
from app.rest_api.api.clubPosting import clubPosting_router
from app.rest_api.api.chat import chat_router


rest_router = APIRouter()
rest_router.include_router(user_router)
rest_router.include_router(province_router)
rest_router.include_router(position_router)
rest_router.include_router(banner_router)
rest_router.include_router(faq_router)
rest_router.include_router(match_router)
rest_router.include_router(guest_router)
rest_router.include_router(club_router)
rest_router.include_router(clubPosting_router)
rest_router.include_router(chat_router)
