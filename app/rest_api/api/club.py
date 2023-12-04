from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user

from app.model.club import Club, JoinClub

from app.rest_api.schema.club import ClubSchema, UpdateClubSchema, FilterClubSchema


club_router = APIRouter(tags=["club"], prefix="/club")


@club_router.post("/create")
def create_club(
    club_data: ClubSchema,
    token: Annotated[str, Depends(get_current_user)],
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
        uniform_color=club_data.uniform_color,
    )
    db.add(club_data)
    db.commit()
    db.refresh(club_data)

    join_club_data = JoinClub(clubs_seq=club_data.seq, user_seq=token.seq, role="회장")
    db.add(join_club_data)
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
            setattr(club, key, value)

        db.commit()
        db.refresh(club)

    return {"success": True}


@club_router.post("/filter")
def filter_club(
    filter_items: FilterClubSchema,
    db: Session = Depends(get_db),
):
    query = db.query(
        Club.name, Club.location, Club.age_group, Club.skill, Club.membership_fee
    )

    for key, value in filter_items.dict(exclude_none=True).items():
        if hasattr(Club, key):
            query = query.filter(getattr(Club, key) == value)

    offset = (filter_items.page - 1) * filter_items.per_page
    query = query.limit(filter_items.per_page).offset(offset)

    clubs = [
        {
            "name": name,
            "location": location,
            "age_group": age_group,
            "skill": skill,
            "membership_fee": membership_fee,
        }
        for name, location, age_group, skill, membership_fee in query.all()
    ]

    return clubs
