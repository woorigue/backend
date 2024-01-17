from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user
from app.core import rabbitmq_helper
from app.model.chat import ChattingRoom, ChattingContent, UserChatRoomAssociation
from app.rest_api.schema.chat import CreateMatchChatRoomSchema, CreateMatchChatSchema


chat_router = APIRouter(tags=["chat"], prefix="/chat")


@chat_router.post("/match")
def create_match_chat_room(
    user_data: CreateMatchChatRoomSchema,  # TODO: serach for user to get club owner's user seq value
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    from datetime import datetime

    chatting_room = ChattingRoom(created_at=datetime.utcnow())

    db.add(chatting_room)
    db.commit()
    db.flush()

    # TODO: add user field in match table
    association_data = {
        "userId": token.seq,
        "chat_room_seq": chatting_room.seq,
        "joinDate": datetime.utcnow(),  # 현재 시간을 joinDate로 설정
    }
    user_chatroom_association_insert = UserChatRoomAssociation.insert().values(
        **association_data
    )
    db.execute(user_chatroom_association_insert)
    db.add(chatting_room)
    db.commit()

    return {"chat_room_seq": chatting_room.seq}


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

    rabbitmq_helper.publish(str(chat_room_id), user_data.contents, token.seq)

    return {"success": True}


@chat_router.get("/match/{chat_room_id}")
def create_match_chat(
    chat_room_id: int,
    # token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    contents = (
        db.query(ChattingContent)
        .filter(ChattingContent.chatting_room_seq == chat_room_id)
        .all()
    )
    return contents
