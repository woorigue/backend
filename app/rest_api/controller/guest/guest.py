from sqlalchemy.orm import Session

from app.model.guest import Guest
from app.rest_api.schema.guest.guest import GuestRegisterSchema


class GuestController:
    def register_guest(self, guest_data: GuestRegisterSchema, db: Session) -> None:
        ("----guest_data---", guest_data)
        Guest.create(guest_data, db)


guest_controller = GuestController()
