from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.orm import Session, aliased

# from app.core import rabbitmq_helper
from app.core.deps import get_db
from app.core.token import get_current_user
from app.model.chat import ChattingContent, ChattingRoom, UserChatRoomAssociation
from app.model.profile import Profile
from app.model.user import User
from app.rest_api.schema.chat import CreateMatchChatSchema

chat_router = APIRouter(tags=["chat"], prefix="/chat")


@chat_router.post("/match/{chat_room_id}")
def create_match_chat(
    chat_room_id: int,
    user_data: CreateMatchChatSchema,  # TODO: serach for user to get club owner's user seq value
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    chatting_contents = ChattingContent(
        chatting_room_seq=chat_room_id, user_seq=token.seq, content=user_data.contents
    )
    db.add(chatting_contents)
    db.commit()
    db.flush()

    # rabbitmq_helper.publish(str(chat_room_id), user_data.contents, [])

    return {"success": True}


@chat_router.get("/match/{chat_room_id}")
def get_match_chats(
    chat_room_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    contents = (
        db.query(ChattingContent)
        .filter(ChattingContent.chatting_room_seq == chat_room_id)
        .all()
    )
    return contents


@chat_router.delete("/match/{chat_room_id}/leave")
def get_match_chats(
    chat_room_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    chat_associate = (
        db.query(UserChatRoomAssociation)
        .filter(
            UserChatRoomAssociation.userId == token.seq,
            UserChatRoomAssociation.chat_room_seq == chat_room_id,
        )
        .first()
    )

    if chat_associate:
        chat_associate.leave = True
        db.add(chat_associate)
        db.commit()

    return {"success": True}


@chat_router.get("")
def get_joined_chat_list(
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    LastMessage = aliased(ChattingContent)
    OtherUser = aliased(User)
    OtherProfile = aliased(Profile)
    last_message_subquery = (
        select(
            ChattingContent.chatting_room_seq,
            func.max(ChattingContent.created_at).label("max_created_at"),
        )
        .group_by(ChattingContent.chatting_room_seq)
        .subquery()
    )

    query = (
        select(
            ChattingRoom.seq,
            LastMessage.content,
            LastMessage.created_at,
            OtherProfile.nickname,
            OtherProfile.img,
        )
        .join(User.chatting_rooms)
        .outerjoin(
            last_message_subquery,
            ChattingRoom.seq == last_message_subquery.c.chatting_room_seq,
        )
        .outerjoin(
            LastMessage,
            (LastMessage.chatting_room_seq == ChattingRoom.seq)
            & (LastMessage.created_at == last_message_subquery.c.max_created_at),
        )
        .join(
            UserChatRoomAssociation,
            UserChatRoomAssociation.chat_room_seq == ChattingRoom.seq,
        )
        .join(
            OtherUser,
            (OtherUser.seq == UserChatRoomAssociation.userId)
            & (OtherUser.seq != User.seq),
        )
        .outerjoin(OtherProfile, OtherUser.seq == OtherProfile.user_seq)
        .filter(User.seq == token.seq)
    )

    result = db.execute(query)

    chat_list = []
    for (
        chatting_room,
        last_message,
        last_message_created,
        user_nickname,
        user_img,
    ) in result:
        chat_list.append(
            {
                "other_user": {
                    "user_name": jsonable_encoder(user_nickname),
                    "user_img": jsonable_encoder(user_img),
                },
                "chatting_room": jsonable_encoder(chatting_room),
                "data": {
                    "last_message": jsonable_encoder(last_message)
                    if last_message
                    else None,
                    "created": jsonable_encoder(last_message_created),
                },
            }
        )

    return chat_list
