from sqlalchemy import Column, String, Integer, DateTime

from app.db.session import Base
from sqlalchemy.orm import Session

from datetime import datetime

from app.rest_api.schema.notification.faq import FaqCreateSchema, FaqEditSchema
from app.helper.exception import FaqNotFoundException

import bleach


class Faq(Base):
    __tablename__ = "faq"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    title = Column(String(255), nullable=False, comment="제목")
    body = Column(String(255), nullable=False, comment="본문")
    create_date = Column(DateTime, nullable=False, comment="생성일자")

    @staticmethod
    def create(faq_data: FaqCreateSchema, db: Session) -> None:
        # HTML 콘텐츠 정화
        clean_title = bleach.clean(faq_data.title)
        clean_body = bleach.clean(faq_data.body)

        # 데이터베이스에 저장
        faq = Faq(title=clean_title, body=clean_body, create_date=datetime.now())
        db.add(faq)
        db.commit()

    @staticmethod
    def edit(faq_id: int, faq_data: FaqEditSchema, db: Session) -> None:
        faq = db.query(Faq).filter(Faq.seq == faq_id).first()
        print(faq, faq_data)
        if not faq:
            raise FaqNotFoundException

        for key, value in faq_data.dict(exclude_unset=True).items():
            if value is not None:
                cleaned_value = bleach.clean(value) if isinstance(value, str) else value
                setattr(faq, key, cleaned_value)

        db.commit()
