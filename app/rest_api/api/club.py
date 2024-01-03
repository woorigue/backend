from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user

from app.model.club import Club, JoinClub

from app.rest_api.schema.club import ClubSchema, UpdateClubSchema

club_router = APIRouter(tags=["club"], prefix="/club")


@club_router.post("")
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


@club_router.patch("/{club_seq}")
def update_club(
    club_seq: int,
    update_club_data: UpdateClubSchema,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter_by(seq=club_seq).first()

    if club:
        for key, value in update_club_data.dict(exclude_none=True).items():
            setattr(club, key, value)

        db.commit()
        db.refresh(club)

    return {"success": True}


@club_router.get("")
def query_clubs(
    seq: int = Query(None, title="클럽 시퀸스"),
    name: str = Query(None, title="클럽명"),
    location: str = Query(None, title="활동 장소"),
    age_group: str = Query(None, title="나이대"),
    skill: str = Query(None, title="실력"),
    max_membership_fee: int = Query(None, title="최대 회비"),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(
        Club.name, Club.location, Club.age_group, Club.skill, Club.membership_fee
    )

    if seq:
        query = query.filter(Club.seq == seq)
    if name:
        query = query.filter(Club.name == name)
    if location:
        query = query.filter(Club.location == location)
    if age_group:
        query = query.filter(Club.age_group == age_group)
    if skill:
        query = query.filter(Club.skill == skill)
    if max_membership_fee:
        query = query.filter(Club.membership_fee <= max_membership_fee)

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
