from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user
from app.core.utils import error_responses
from app.helper.exception import ClubPostingCreatePermissionDenied
from app.model.clubPosting import ClubPosting, JoinClubPosting
from app.model.club import Club
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.club.clubPosting import (
    ClubPostingSchema,
    FilterClubPostingSchema,
    UpdateClubPostingSchema,
)
from app.model.notification import Notification
from app.model.device import Device
from firebase_admin import messaging
from app.rest_api.schema.notification.notification import (
    CreateNotificationSchema,
    NotificationType,
)

clubPosting_router = APIRouter(
    tags=["clubPosting"], prefix="/clubPosting", deprecated=True
)


@clubPosting_router.post(
    "",
    summary="클럽 모집 공고글 생성",
    response_model=CreateResponse,
    responses={
        400: {"description": error_responses([ClubPostingCreatePermissionDenied])}
    },
)
def create_clubPosting(
    clubPosting_data: ClubPostingSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    from app.model.club import JoinClub

    join_club = (
        db.query(JoinClub.clubs_seq)
        .filter(JoinClub.user_seq == token.seq, JoinClub.role == "owner")
        .all()
    )
    club_seq_list = [item[0] for item in join_club]

    if clubPosting_data.club_seq not in club_seq_list:
        raise ClubPostingCreatePermissionDenied

    clubPosting_data = ClubPosting(
        date=datetime.now(),
        club_seq=clubPosting_data.club_seq,
        title=clubPosting_data.title,
        notice=clubPosting_data.notice,
        recruitment_number=clubPosting_data.recruitment_number,
        location=clubPosting_data.location,
        age_group=clubPosting_data.age_group,
        membership_fee=clubPosting_data.membership_fee,
        level=clubPosting_data.level,
        gender=clubPosting_data.gender,
        user_seq=token.seq,
    )
    db.add(clubPosting_data)
    db.commit()

    join_clubPosting_data = JoinClubPosting(
        club_posting_seq=clubPosting_data.seq,
        club_seq=clubPosting_data.club_seq,
        user_seq=token.seq,
        accepted=False,
    )
    db.add(join_clubPosting_data)
    db.commit()

    return {"success": True}


@clubPosting_router.get(
    "/{club_posting_seq}",
    summary="클럽 모집 공고글 상세 조회",
    response_model=CreateResponse,
)
def get_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_seq: int,
    db: Session = Depends(get_db),
):
    club_posting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )

    return club_posting


@clubPosting_router.patch(
    "/{club_posting_seq}", summary="클럽 모집글 수정", response_model=CreateResponse
)
def update_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_seq: int,
    update_club_posting_data: UpdateClubPostingSchema,
    db: Session = Depends(get_db),
):
    club_posting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )

    for key, value in update_club_posting_data.dict(exclude_none=True).items():
        setattr(club_posting, key, value)

    db.commit()

    return {"success": True}


@clubPosting_router.get("", summary="클럽 모집글 조회")
def filter_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_filter: FilterClubPostingSchema = FilterDepends(
        FilterClubPostingSchema
    ),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(ClubPosting)
    query = club_posting_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    club_posting = query.all()
    return club_posting


@clubPosting_router.delete(
    "/{club_posting_seq}",
    summary="클럽 모집 공고글 삭제",
    response_model=CreateResponse,
)
def delete_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_seq: int,
    db: Session = Depends(get_db),
):
    clubPosting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )

    db.delete(clubPosting)
    db.commit()

    return {"success": True}


@clubPosting_router.post(
    "/{club_posting_seq}/join",
    summary="클럽 공고글 모집 신청",
    response_model=CreateResponse,
)
def join_clubPosting(
    club_posting_seq: int,
    club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    club_posting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )

    join_club_posting = JoinClubPosting(
        club_posting_seq=club_posting.seq,
        club_seq=club_seq,
        user_seq=token.seq,
        accepted=False,
    )
    db.add(join_club_posting)
    db.commit()

    device_info = (
        db.query(Device).filter(Device.user_seq == club_posting.user_seq).first()
    )
    if device_info:
        club = db.query(Club).filter(Club.seq == club_seq).first()
        club_data = {
            "club_seq": club_seq,
            "club_name": club.name,
            "publisher_name": token.profile[0].nickname,
        }
        notification_schema = CreateNotificationSchema(
            type=NotificationType.CLUB_REQUEST,
            title="클럽 입단 신청",
            message="클럽 입단 신청이 들어왔습니다",
            from_user_seq=token.seq,
            to_user_seq=device_info.user_seq,
            data=club_data,
        )
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification_schema.title, body=notification_schema.message
            ),
            token=device_info.token,
        )
        messaging.send(message)
        notification = Notification(**notification_schema.model_dump())
        db.add(notification)
        db.commit()

        test = db.query(Notification).filter(Notification.seq == 46).first()
        print(test.data)

    return {"success": True}


@clubPosting_router.patch(
    "/{club_posting_seq}/accept",
    summary="클럽 공고글 수락",
    response_model=CreateResponse,
)
def join_clubPosting(
    club_posting_seq: int,
    club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    club_posting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )
    join_club_posting = (
        db.query(JoinClubPosting)
        .filter(
            JoinClubPosting.club_posting_seq == club_posting.seq,
            JoinClubPosting.club_seq == club_seq,
            JoinClubPosting.user_seq == token.seq,
        )
        .first()
    )
    join_club_posting.accepted = True
    db.commit()
    return {"success": True}
