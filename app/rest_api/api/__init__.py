from fastapi import APIRouter

from app.rest_api.api.banner import banner_router
from app.rest_api.api.chat import chat_router
from app.rest_api.api.club.club import club_router
from app.rest_api.api.club.clubPosting import clubPosting_router
from app.rest_api.api.guest.guest import guest_router
from app.rest_api.api.match.match import match_router
from app.rest_api.api.memberPosting import memberPosting_router
from app.rest_api.api.notification.faq import faq_router
from app.rest_api.api.poll import poll_router
from app.rest_api.api.position import position_router
from app.rest_api.api.province import province_router
from app.rest_api.api.user import user_router
from app.rest_api.api.firebase.firebase import firebase_router

health_check_router = APIRouter(prefix="")


@health_check_router.get("/")
def health_check():
    return 200


rest_router = APIRouter()
rest_router.include_router(health_check_router)
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
rest_router.include_router(poll_router)
rest_router.include_router(memberPosting_router)
rest_router.include_router(firebase_router)
