from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user

from app.model.clubPosting import ClubPosting, JoinClubPosting
from app.rest_api.schema.club.clubPosting import (
    ClubPostingSchema,
    UpdateClubPostingSchema,
    FilterClubPostingSchema,
)

clubPosting_router = APIRouter(tags=["clubPosting"], prefix="/clubPosting")


@clubPosting_router.post("")
def create_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    clubPosting_data: ClubPostingSchema,
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

    join_clubPosting_data = JoinClubPosting(
        club_posting_seq=clubPosting_data.seq,
        club_seq=clubPosting_data.club_seq,
        user_seq=token.seq,
        accepted=False,
    )
    db.add(join_clubPosting_data)
    db.commit()

    return {"success": True}


@clubPosting_router.get("/{club_posting_seq}")
def get_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_seq: int,
    db: Session = Depends(get_db),
):
    club_posting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )

    # if club_posting is None:
    #     raise ClubPostingNotFoundException

    return club_posting


@clubPosting_router.patch("/{club_posting_seq}")
def update_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_seq: int,
    update_club_posting_data: UpdateClubPostingSchema,
    db: Session = Depends(get_db),
):
    club_posting = (
        db.query(ClubPosting).filter_by(ClubPosting.seq == club_posting_seq).first()
    )

    # if not club:
    #     raise ClubNotFoundException

    for key, value in update_club_posting_data.dict(exclude_none=True).items():
        setattr(club_posting, key, value)

    db.commit()

    return {"success": True}


@clubPosting_router.get("")
def filter_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
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


@clubPosting_router.delete("/{club_posting_seq}")
def delete_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    club_posting_seq: int,
    db: Session = Depends(get_db),
):
    clubPosting = (
        db.query(ClubPosting).filter(ClubPosting.seq == club_posting_seq).first()
    )

    # if not clubPosting:
    #     raise clubPostingNotFoundException

    db.delete(clubPosting)
    db.commit()

    return {"message": "매치게시글이 성공적으로 삭제되었습니다."}
