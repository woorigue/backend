from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user

from app.model.clubPosting import ClubPosting, JoinClubPosting

from app.rest_api.schema.clubPosting import (
    ClubPostingSchema,
    UpdateClubPostingSchema,
    FilterClubPostingSchema,
)

clubPosting_router = APIRouter(tags=["clubPosting"], prefix="/clubPosting")


@clubPosting_router.post("")
def create_clubPosting(
    clubPosting_data: ClubPostingSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    clubPosting_data = ClubPosting(
        club_seq=clubPosting_data.club_seq,
        title=clubPosting_data.title,
        intro=clubPosting_data.intro,
        recruitment_number=clubPosting_data.recruitment_number,
        location=clubPosting_data.location,
        age_group=clubPosting_data.age_group,
        membership_fee=clubPosting_data.membership_fee,
        skill=clubPosting_data.skill,
        gender=clubPosting_data.gender,
        status=clubPosting_data.status,
        user_seq=token.seq,
    )
    db.add(clubPosting_data)
    db.commit()
    db.refresh(clubPosting_data)

    join_clubPosting_data = JoinClubPosting(
        club_posting_seq=clubPosting_data.seq,
        club_seq=clubPosting_data.club_seq,
        user_seq=token.seq,
        accepted=False,
    )
    db.add(join_clubPosting_data)
    db.commit()
    db.flush()

    return {"success": True}


@clubPosting_router.patch("/{club_posting_seq}")
def update_clubPosting(
    club_posting_seq: int,
    update_club_data: UpdateClubPostingSchema,
    db: Session = Depends(get_db),
):
    club = db.query(ClubPosting).filter_by(seq=club_posting_seq).first()

    if club:
        for key, value in update_club_data.dict(exclude_none=True).items():
            setattr(club, key, value)

        db.commit()
        db.refresh(club)

    return {"success": True}


@clubPosting_router.get("")
def query_clubPosting(
    club_posting_filter: FilterClubPostingSchema = FilterDepends(
        FilterClubPostingSchema
    ),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(ClubPosting)
    query = club_posting_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)

    club_posting = query.all()

    return club_posting
