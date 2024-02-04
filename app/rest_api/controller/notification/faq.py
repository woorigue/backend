from sqlalchemy.orm import Session

from app.model.faq import Faq
from app.rest_api.schema.notification.faq import FaqCreateSchema, FaqEditSchema


class FaqController:
    def create_faq(self, faq_data: FaqCreateSchema, db: Session) -> None:
        Faq.create(faq_data, db)

    def edit_faq(self, faq_id: int, faq_data: FaqEditSchema, db: Session) -> None:
        Faq.edit(faq_id, faq_data, db)


faq_controller = FaqController()
