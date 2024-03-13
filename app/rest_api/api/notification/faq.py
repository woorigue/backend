from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.model.faq import Faq
from typing import Annotated
from app.core.token import (
    get_current_user,
)

# Schema
from app.rest_api.schema.notification.faq import (
    FaqCreateSchema,
    FaqEditSchema,
)

# Controller
from app.rest_api.controller.notification.faq import faq_controller as con

from app.helper.exception import FaqNotFoundException

faq_router = APIRouter(tags=["faq"], prefix="/faq")


@faq_router.get("")
def list_faqs(db: Session = Depends(get_db)):
    faq = db.query(Faq).order_by(Faq.create_date.desc()).all()
    return faq


@faq_router.get("/{faq_id}")
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = db.query(Faq).filter(Faq.seq == faq_id).first()
    if faq is None:
        raise FaqNotFoundException
    return faq


@faq_router.post("")
def create_faq(
    faq_data: FaqCreateSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    con.create_faq(faq_data, db)
    return {"success": True}


@faq_router.patch("/{faq_id}")
def edit_faq(
    faq_id: int,
    faq_data: FaqEditSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    con.edit_faq(faq_id, faq_data, db)
    return {"success": True}


@faq_router.delete("/{faq_id}")
def delete_faq(
    faq_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    faq = db.query(Faq).filter(Faq.seq == faq_id).first()
    if not faq:
        raise FaqNotFoundException

    db.delete(faq)
    db.commit()
    return {"success": True}
