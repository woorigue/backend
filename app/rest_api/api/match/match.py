from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session, joinedload
from firebase_admin import messaging

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)
from app.core.utils import error_responses
from app.helper.exception import (
    ClubPermissionException,
    MatchNotFoundException,
    RegisterMatchError,
    JoinMatchException,
    JoinMatchNotFoundException,
    JoinMatchAcceptException,
    MatchExpiredException,
)

from app.model.club import Club
from app.model.match import JoinMatch, Match
from app.model.device import Device
from app.model.notification import Notification

from app.rest_api.controller.club import ClubController
from app.rest_api.controller.match.match import MatchController
from app.rest_api.controller.poll import PollController

from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.match.match import (
    FilterMatchSchema,
    MatchResponseSchema,
    MatchSchema,
    UpdateMatchSchema,
)
from app.rest_api.schema.poll import (
    CreatePollSchema,
)
from app.rest_api.schema.notification.notification import (
    CreateNotificationSchema,
    NotificationType,
)

# from app.core import rabbitmq_helper
from app.model.chat import ChattingRoom, UserChatRoomAssociation, ChattingContent
from app.rest_api.schema.match.match import JoinMatchResponseSchema
from datetime import datetime
from app.rest_api.controller.notification.notification import MatchNotificationService


match_router = APIRouter(tags=["match"], prefix="/match")


@match_router.post(
    "",
    summary="매치 생성",
    responses={400: {"description": error_responses([RegisterMatchError])}},
    response_model=CreateResponse,
)
def create_match(
    token: Annotated[str, Depends(get_current_user)],
    match_data: MatchSchema,
    db: Session = Depends(get_db),
):
    controller = MatchController(db)
    is_validate = controller.validate_match_register(match_data, token.seq)

    if not is_validate:
        raise RegisterMatchError

    if match_data.match_type == "private":
        match_status = "found"
    else:
        match_status = "pending"

    match = Match(
        date=datetime.now(),
        user_seq=token.seq,
        home_club_seq=match_data.home_club_seq,
        match_type=match_data.match_type,
        location=match_data.location,
        match_date=match_data.match_date,
        start_time=match_data.start_time,
        end_time=match_data.end_time,
        level=match_data.level,
        team_size=match_data.team_size,
        gender=match_data.gender,
        match_fee=match_data.match_fee,
        notice=match_data.notice,
        latitude=match_data.latitude,
        longitude=match_data.longitude,
    )
    db.add(match)
    db.commit()

    poll_data = CreatePollSchema(
        match_seq=match.seq,
        club_seq=match.home_club_seq,
        expired_at=datetime.combine(match.match_date, match.end_time),
    )
    poll_controller = PollController(token, db)
    poll = poll_controller.create_poll(poll_data)
    match.home_club_poll_seq = poll.seq

    db.commit()

    return {"success": True}


@match_router.get(
    "/{match_seq}",
    summary="매치 세부 조회",
    responses={404: {"description": error_responses([MatchNotFoundException])}},
    response_model=MatchResponseSchema,
)
def get_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    db: Session = Depends(get_db),
):
    match = (
        db.query(Match)
        .options(
            joinedload(Match.home_club),
            joinedload(Match.away_club),
            joinedload(Match.home_club_guest),
            joinedload(Match.away_club_guest),
        )
        .filter(Match.seq == match_seq)
        .first()
    )

    if match is None:
        raise MatchNotFoundException

    return match


@match_router.patch(
    "/{match_seq}",
    summary="매치 수정",
    responses={404: {"description": error_responses([MatchNotFoundException])}},
    response_model=CreateResponse,
)
def update_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    match_data: UpdateMatchSchema,
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()

    if not match:
        raise MatchNotFoundException

    for key, value in match_data.dict(exclude_none=True).items():
        setattr(match, key, value)

    db.commit()

    return {"success": True}


@match_router.delete(
    "/{match_seq}",
    summary="매치 삭제",
    responses={404: {"description": error_responses([MatchNotFoundException])}},
    response_model=CreateResponse,
)
def delete_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()

    if not match:
        raise MatchNotFoundException

    db.delete(match)
    db.commit()

    return {"success": True}


@match_router.get("", response_model=list[MatchResponseSchema], summary="매치 조회")
def filter_match(
    token: Annotated[str, Depends(get_current_user)],
    match_filter: FilterMatchSchema = FilterDepends(FilterMatchSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Match).filter(
        Match.matched == False,
        Match.match_date + Match.start_time > datetime.now(),
    )
    query = match_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    matches = query.all()
    return matches


@match_router.post(
    "/{match_seq}/join",
    summary="매치 참여",
    responses={404: {"description": error_responses([MatchNotFoundException])}},
    response_model=CreateResponse,
)
def join_match(
    match_seq: int,
    away_club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()
    if not match:
        raise MatchNotFoundException

    now = datetime.now()
    if match.match_date < now:
        raise MatchExpiredException

    if match.away_club_seq is not None:
        raise MatchNotFoundException

    if match.home_club_seq == away_club_seq:
        raise JoinMatchException

    join_match = JoinMatch(
        match_seq=match.seq,
        user_seq=token.seq,
        away_club_seq=away_club_seq,
        accepted=False,
    )
    db.add(join_match)
    db.commit()

    # # 채팅방 생성 로직
    # chatting_room = ChattingRoom(created_at=datetime.utcnow())
    # db.add(chatting_room)
    # db.commit()
    # db.flush()

    # # 채팅방 참여 로직
    # association_data = {
    #     "userId": token.seq,
    #     "chat_room_seq": chatting_room.seq,
    #     "joinDate": datetime.utcnow(),  # 현재 시간을 joinDate로 설정
    # }
    # chat_association = UserChatRoomAssociation(**association_data)
    # db.add(chat_association)
    # db.commit()

    # association_data = {
    #     "userId": match.user_seq,
    #     "chat_room_seq": chatting_room.seq,
    #     "joinDate": datetime.utcnow(),  # 현재 시간을 joinDate로 설정
    # }
    # chat_association = UserChatRoomAssociation(**association_data)
    # db.add(chat_association)
    # db.commit()
    #
    # chatting_contents = ChattingContent(
    #     chatting_room_seq=chatting_room.seq,
    #     user_seq=token.seq,
    #     content="매칭 우리 함께해요",
    # )
    # db.add(chatting_contents)
    # db.commit()
    # db.flush()

    # user_id = [match.user_seq]
    # rabbitmq_helper.publish(chatting_room.seq, chatting_contents.content, user_id)

    # away_club = db.query(Club).filter(Club.seq == away_club_seq).first()
    # data = {
    #     "away_club_seq": away_club.seq,
    #     "away_club_name": away_club.name,
    #     "match_seq": match.seq,
    #     "match_date": match.match_date.strftime("%Y-%m-%d"),
    # }
    # notification_schema = CreateNotificationSchema(
    #     type=NotificationType.MATCH_REQUEST.value,
    #     title="매치 신청 알림",
    #     message="매치 신청이 도착했습니다.",
    #     from_user_seq=token.seq,
    #     to_user_seq=match.user_seq,
    #     data=data,
    # )
    #
    # notification = Notification(**notification_schema.model_dump())
    # db.add(notification)
    # db.commit()
    #
    # device_info = db.query(Device).filter(Device.user_seq == match.user_seq).first()
    # if device_info:
    #     message = messaging.Message(
    #         notification=messaging.Notification(
    #             title=notification_schema.title, body=notification_schema.message
    #         ),
    #         token=device_info.token,
    #     )
    #     messaging.send(message)

    service = MatchNotificationService(match)
    service.send(token, db)

    return {"success": True}


@match_router.patch(
    "/{match_seq}/accept",
    summary="매치 수락",
    responses={
        404: {
            "description": error_responses(
                [
                    MatchNotFoundException,
                    JoinMatchNotFoundException,
                    JoinMatchAcceptException,
                ]
            )
        }
    },
    response_model=CreateResponse,
)
def accept_match(
    match_seq: int,
    away_club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()
    join_match = (
        db.query(JoinMatch)
        .filter(
            JoinMatch.match_seq == match_seq, JoinMatch.away_club_seq == away_club_seq
        )
        .first()
    )

    if not match:
        raise MatchNotFoundException

    if not join_match:
        raise JoinMatchNotFoundException

    club_con = ClubController(token)
    is_owner = club_con.is_owner(db, match.home_club_seq)
    if not is_owner:
        raise ClubPermissionException

    match.matched = True
    match.away_club_seq = away_club_seq

    if join_match.accepted:
        raise JoinMatchAcceptException

    join_match.accepted = True

    poll_data = CreatePollSchema(
        match_seq=match.seq,
        club_seq=match.away_club_seq,
        expired_at=datetime.combine(match.match_date, match.end_time),
    )
    poll_controller = PollController(token, db)
    poll = poll_controller.create_poll(poll_data)
    match.away_club_poll_seq = poll.seq

    db.commit()

    return {"success": True}
