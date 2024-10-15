from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Boolean

from app.core.model import TimestampedModel


class Notification(TimestampedModel):
    __tablename__ = "notification"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    type = Column(String(128), comment="알림 타입")
    from_user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    to_user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    title = Column(String(128), comment="제목")
    message = Column(String(128), comment="메시지")
    data = Column(JSON, default=dict, comment="데이터")
    is_read = Column(Boolean, default=False, comment="읽음 처리")
