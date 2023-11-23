from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.deps import get_db

from app.model.clubs import Club

from app.rest_api.schema.club import ClubSchema, UpdateClubSchema, DeleteClubSchema


club_router = APIRouter(tags=["club"], prefix="/club")


@club_router.post("/create")
def create_club(
    club_data: ClubSchema,
    db: Session = Depends(get_db),
):
    club_data = Club(
        name=club_data.name,
        register_date=club_data.register_date,
        location=club_data.location,
        age_group=club_data.age_group,
        membership_fee=club_data.membership_fee,
        skill=club_data.skill,
        img=club_data.img,
        color=club_data.color,
    )

    db.add(club_data)
    db.commit()
    db.refresh(club_data)
    db.commit()
    db.flush()
    return {"success": True}


@club_router.patch("/update")
def update_club(
    update_club_data: UpdateClubSchema,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter_by(seq=update_club_data.seq).first()

    if club:
        for key, value in update_club_data.dict(exclude_none=True).items():
            print(key, value)
            setattr(club, key, value)

        db.commit()
        db.refresh(club)

    return {"success": True}


@club_router.delete("/delete")
def update_club(
    delete_club_data: DeleteClubSchema,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter_by(seq=delete_club_data.seq).first()

    if club:
        db.delete(club)
        db.commit()
        return {"success": True}
