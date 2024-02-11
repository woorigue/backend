from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user

from app.model.club import Club, JoinClub
from app.rest_api.schema.club.club import (
    ClubSchema,
    UpdateClubSchema,
    FilterClubSchema,
)

club_router = APIRouter(tags=["club"], prefix="/club")


@club_router.post("")
def create_club(
    token: Annotated[str, Depends(get_current_user)],
    club_data: ClubSchema,
    db: Session = Depends(get_db),
):
    club = Club(
        name=club_data.name,
        register_date=club_data.register_date,
        location=club_data.location,
        age_group=club_data.age_group,
        membership_fee=club_data.membership_fee,
        skill=club_data.skill,
        img=club_data.img,
        uniform_color=club_data.uniform_color,
    )
    db.add(club)
    db.commit()

    join_club = JoinClub(clubs_seq=club.seq, user_seq=token.seq, role="회장")
    db.add(join_club)
    db.commit()

    return {"success": True}


@club_router.get("/{club_seq}")
def get_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    # if club is None:
    #     raise ClubNotFoundException

    return club


@club_router.patch("/{club_seq}")
def update_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    update_club_data: UpdateClubSchema,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    # if not club:
    #     raise ClubNotFoundException

    for key, value in update_club_data.dict(exclude_none=True).items():
        setattr(club, key, value)

    db.commit()

    return {"success": True}


@club_router.get("")
def filter_clubs(
    token: Annotated[str, Depends(get_current_user)],
    club_filter: FilterClubSchema = FilterDepends(FilterClubSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(
        Club.name, Club.location, Club.age_group, Club.skill, Club.membership_fee
    )
    query = club_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)

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


@club_router.delete("/{club_seq}")
def delete_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    # if not club:
    #     raise ClubNotFoundException

    db.delete(club)
    db.commit()

    return {"message": "클럽이 성공적으로 삭제되었습니다."}
