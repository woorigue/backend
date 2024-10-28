from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi_filter import FilterDepends
from sqlalchemy import and_, delete, exists, or_
from sqlalchemy.orm import Session, joinedload
from firebase_admin import messaging

from app.core.deps import get_db
from app.core.token import get_current_user
from app.core.utils import error_responses
from app.helper.exception import (
    ClubNotFoundException,
    ClubPermissionException,
    JoinClubLimitError,
    JoinClubNotFoundException,
    JoinClubAcceptException,
)
from app.model.club import Club, JoinClub
from app.model.match import Match
from app.model.position import JoinPosition
from app.model.profile import Profile
from app.model.notification import Notification
from app.model.device import Device

from app.rest_api.controller.club import ClubController
from app.rest_api.controller.file import file_controller as file_con
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.club.club import (
    ClubListSchema,
    ClubResponseSchema,
    FilterClubSchema,
    GetClubMemberSchema,
    CreateClubResponse,
)
from app.rest_api.schema.profile import GetProfileSchema
from app.rest_api.schema.notification.notification import (
    CreateNotificationSchema,
    NotificationType,
)


club_router = APIRouter(tags=["club"], prefix="/club")


@club_router.post(
    "",
    summary="클럽 생성",
    responses={400: {"description": error_responses([JoinClubLimitError])}},
    response_model=CreateClubResponse,
)
async def create_club(
    token: Annotated[str, Depends(get_current_user)],
    emblem_img: UploadFile | None = File(None),
    img: UploadFile | None = File(None),
    level: int = Form(...),
    register_date: str = Form(...),
    intro: str = Form(...),
    name: str = Form(...),
    location: str = Form(...),
    gender: str = Form(...),
    uniform_color: str = Form(...),
    membership_fee: int = Form(...),
    age_group: str = Form(...),
    db: Session = Depends(get_db),
):
    con = ClubController(token)
    join_club_count = con.get_joined_club_count(db)
    if join_club_count >= 2:
        raise JoinClubLimitError

    emblem_url = ""
    if emblem_img is not None:
        emblem_contents = await emblem_img.read()
        emblem_url = file_con.upload_club_img(emblem_contents, emblem_img.filename)

    img_url = ""
    if img is not None:
        img_contents = await img.read()
        img_url = file_con.upload_club_img(img_contents, img.filename)

    club = Club(
        name=name,
        register_date=register_date,
        intro=intro,
        location=location,
        age_group=age_group,
        membership_fee=membership_fee,
        level=level,
        gender=gender,
        emblem_img=emblem_url,
        img=img_url,
        uniform_color=uniform_color,
    )
    db.add(club)
    db.commit()

    join_club = JoinClub(
        clubs_seq=club.seq, user_seq=token.seq, role="owner", accepted=True
    )
    db.add(join_club)
    db.commit()

    return {"club_seq": club.seq}


@club_router.get(
    "/{club_seq}",
    summary="클럽 상세 조회",
    response_model=ClubResponseSchema,
    responses={404: {"description": error_responses([ClubNotFoundException])}},
)
def get_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    if club is None:
        raise ClubNotFoundException

    return club


@club_router.patch(
    "/{club_seq}",
    summary="클럽 정보 수정",
    response_model=CreateResponse,
    responses={
        400: {"description": error_responses([ClubPermissionException])},
        404: {"description": error_responses([ClubNotFoundException])},
    },
)
async def update_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    emblem_img: UploadFile | None = File(None),
    img: UploadFile | None = File(None),
    level: int = Form(...),
    register_date: str = Form(...),
    intro: str = Form(...),
    name: str = Form(...),
    location: str = Form(...),
    gender: str = Form(...),
    uniform_color: str = Form(...),
    membership_fee: int = Form(...),
    age_group: str = Form(...),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()
    if club is None:
        raise ClubNotFoundException

    con = ClubController(token)
    is_owner = con.is_owner(db, club_seq)
    if not is_owner:
        raise ClubPermissionException

    if emblem_img is None:
        emblem_url = club.emblem_img
    else:
        emblem_contents = await emblem_img.read()
        emblem_url = file_con.upload_club_img(emblem_contents, emblem_img.filename)

    if img is None:
        img_url = club.img
    else:
        img_contents = await img.read()
        img_url = file_con.upload_club_img(img_contents, img.filename)

    club.emblem_img = emblem_url
    club.img = img_url
    club.level = level
    club.register_date = register_date
    club.intro = intro
    club.name = name
    club.location = location
    club.gender = gender
    club.uniform_color = uniform_color
    club.membership_fee = membership_fee
    club.age_group = age_group

    db.commit()

    return {"success": True}


@club_router.delete(
    "/{club_seq}/img",
    summary="클럽 이미지 삭제",
    response_model=CreateResponse,
    responses={
        400: {"description": error_responses([ClubPermissionException])},
        404: {"description": error_responses([ClubNotFoundException])},
    },
)
async def delete_club_image(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    emblem_img: bool,
    img: bool,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()
    if club is None:
        raise ClubNotFoundException

    con = ClubController(token)
    is_owner = con.is_owner(db, club_seq)
    if not is_owner:
        raise ClubPermissionException

    if emblem_img:
        club.emblem_img = None

    if img:
        club.img = None

    db.commit()

    return {"success": True}


@club_router.get("", response_model=list[ClubListSchema], summary="클럽 조회")
def filter_clubs(
    token: Annotated[str, Depends(get_current_user)],
    club_filter: FilterClubSchema = FilterDepends(FilterClubSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    con = ClubController()
    query = db.query(Club).filter(Club.deleted == False)
    query = club_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    clubs = query.all()

    return clubs


@club_router.post("/{club_seq}/join", summary="클럽 가입 신청", response_model=CreateResponse)
def join_club(
    club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    con = ClubController(token)
    join_club_count = con.get_joined_club_count(db)
    if join_club_count >= 2:
        raise JoinClubLimitError

    join_status = db.query(
        exists().where(
            (JoinClub.user_seq == token.seq) & (JoinClub.clubs_seq == club_seq)
        )
    ).scalar()

    if not join_status:
        join_club = JoinClub(user_seq=token.seq, clubs_seq=club_seq, role="member")
        db.merge(join_club)
        db.commit()
        db.flush()

    club = db.query(Club).filter(Club.seq == club_seq).first()
    club_owner = (
        db.query(JoinClub)
        .filter(JoinClub.clubs_seq == club_seq, JoinClub.role == "owner")
        .first()
    )
    data = {
        "club_seq": club_seq,
        "club_name": club.name,
        "publisher_name": token.profile[0].nickname,
    }
    notification_schema = CreateNotificationSchema(
        type=NotificationType.CLUB_REQUEST.value,
        title="클럽 신청 알림",
        message="클럽 신청이 도착했습니다.",
        from_user_seq=token.seq,
        to_user_seq=club_owner.user_seq,
        data=data,
    )
    notification = Notification(**notification_schema.model_dump())
    db.add(notification)
    db.commit()

    device_info = (
        db.query(Device).filter(Device.user_seq == club_owner.user_seq).first()
    )

    if device_info:
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification_schema.title, body=notification_schema.message
            ),
            token=device_info.token,
        )
        messaging.send(message)

    return {"success": True}


@club_router.patch(
    "/{club_seq}/accept",
    summary="클럽 가입 수락",
    responses={
        404: {
            "description": error_responses(
                [ClubNotFoundException, JoinClubNotFoundException]
            )
        }
    },
    response_model=CreateResponse,
)
def accept_club(
    club_seq: int,
    user_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()
    if not club:
        raise ClubNotFoundException

    con = ClubController(token)
    is_owner = con.is_owner(db, club_seq)
    if not is_owner:
        raise ClubPermissionException

    join_club = (
        db.query(JoinClub)
        .filter(
            JoinClub.clubs_seq == club_seq,
            JoinClub.user_seq == user_seq,
        )
        .one()
    )

    if not join_club:
        raise JoinClubNotFoundException

    if join_club.accepted:
        raise JoinClubAcceptException

    join_club.accepted = True
    db.commit()

    return {"success": True}


@club_router.delete("/{club_seq}/quit", summary="클럽 탈퇴", response_model=CreateResponse)
def quit_club(
    club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    join_club = delete(JoinClub).where(
        and_(JoinClub.user_seq == token.seq, JoinClub.clubs_seq == club_seq)
    )
    db.execute(join_club)
    db.commit()
    db.flush()

    return {"success": True}


@club_router.delete(
    "/{club_seq}",
    summary="클럽 삭제",
    responses={
        400: {"description": error_responses([ClubPermissionException])},
        404: {"description": error_responses([ClubNotFoundException])},
    },
    response_model=CreateResponse,
)
def delete_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()
    if club is None:
        raise ClubNotFoundException

    con = ClubController(token)
    is_owner = con.is_owner(db, club_seq)
    if not is_owner:
        raise ClubPermissionException

    club.deleted = True
    db.commit()
    return {"success": True}


@club_router.get(
    "/{club_seq}/members",
    summary="클럽 명단 조회",
    response_model=list[GetClubMemberSchema],
)
def get_members(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    members_query = (
        db.query(Profile, JoinClub.role)
        .join(JoinClub, Profile.user_seq == JoinClub.user_seq)
        .filter(JoinClub.clubs_seq == club_seq, JoinClub.accepted == True)
        .options(joinedload(Profile.join_position).joinedload(JoinPosition.position))
        .all()
    )

    member = [
        GetClubMemberSchema(
            profile=GetProfileSchema.from_orm(member[0]), role=member[1]
        )
        for member in members_query
    ]

    return member


@club_router.delete(
    "/{club_seq}/delete_member",
    summary="클럽 멤버 삭제",
)
def delete_member(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    user_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()
    if club is None:
        raise ClubNotFoundException

    con = ClubController(token)
    is_owner = con.is_owner(db, club_seq)
    if not is_owner:
        raise ClubPermissionException

    join_club = delete(JoinClub).where(
        and_(JoinClub.user_seq == user_seq, JoinClub.clubs_seq == club_seq)
    )
    db.execute(join_club)
    db.commit()
    db.flush()

    return {"success": True}


@club_router.get("/{club_seq}/match_schedule", summary="클럽 매칭 스케줄 조회")
def get_match_schedule(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    today = datetime.today().strftime("%Y-%m-%d")
    match_scehdule = (
        db.query(Match)
        .filter(
            or_(Match.home_club_seq == club_seq, Match.away_club_seq == club_seq),
            Match.match_date >= today,
        )
        .order_by(Match.match_date.asc())
        .all()
    )
    return match_scehdule
