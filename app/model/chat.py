from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from app.db.session import Base

UserChatRoomAssociation = Table(
    "user_chatroom_association",
    Base.metadata,
    Column("userId", Integer, ForeignKey("users.seq"), primary_key=True),
    Column(
        "chat_room_seq",
        Integer,
        ForeignKey("chattingRoom.seq"),
        primary_key=True,
    ),
    Column("joinDate", DateTime, nullable=False, comment="참여 일자"),
)


class ChattingRoom(Base):
    __tablename__ = "chatting_room"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=True, comment="생성 시간"
    )
    # 채팅방에 참여하는 사용자들
    users = relationship(
        "User", secondary=UserChatRoomAssociation, back_populates="chatting_rooms"
    )
    # 채팅방의 메시지 내용
    messages = relationship("ChattingContent", back_populates="chatting_room")


class ChattingContent(Base):
    __tablename__ = "chatting_content"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="메시지 ID")
    chatting_room_seq = Column(
        Integer,
        ForeignKey("chatting_room.seq"),
        nullable=False,
        comment="채팅방 ID",
    )
    user_seq = Column(
        Integer, ForeignKey("users.seq"), nullable=False, comment="사용자 ID"
    )
    content = Column(Text, nullable=False, comment="메시지 내용")
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=True, comment="생성 시간"
    )

    # 메시지를 소유한 채팅방
    chatting_room = relationship("ChattingRoom", back_populates="messages")

    # 메시지를 보낸 사용자
    user = relationship("User")
