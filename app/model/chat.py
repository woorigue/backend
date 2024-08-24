from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table, Text, Boolean
from datetime import datetime

from app.db.session import Base
from sqlalchemy.orm import relationship


class UserChatRoomAssociation(Base):
    __tablename__ = "user_chatroom_association"

    userId = Column(Integer, ForeignKey("users.seq"), primary_key=True)
    chat_room_seq = Column(Integer, ForeignKey("chatting_room.seq"), primary_key=True)
    joinDate = Column(DateTime, nullable=False, comment="참여 일자")
    leave = Column(Boolean, default=False, comment="나가기 여부")

    user = relationship("User", back_populates="chatting_room_associations")
    chatting_room = relationship("ChattingRoom", back_populates="user_associations")


class ChattingRoom(Base):
    __tablename__ = "chatting_room"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=True, comment="생성 시간"
    )

    user_associations = relationship(
        "UserChatRoomAssociation", back_populates="chatting_room"
    )
    users = relationship(
        "User", secondary="user_chatroom_association", back_populates="chatting_rooms"
    )


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

    # # 메시지를 소유한 채팅방
    # chatting_room = relationship("ChattingRoom", back_populates="messages")
    #
    # # 메시지를 보낸 사용자
    # user = relationship("User")
