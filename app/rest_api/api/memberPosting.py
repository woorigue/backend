from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session, joinedload


from app.core.deps import get_db
from app.core.token import get_current_user

from app.model.profile import Profile
from app.model.memberPosting import MemberPosting, JoinMemberPosting
from app.rest_api.schema.memberPosting import (
    MemberPostingSchema,
    UpdateMemberPostingSchema,
    FilterMemberPostingSchema,
)

memberPosting_router = APIRouter(tags=["memberPosting"], prefix="/memberPosting")


@memberPosting_router.post("")
def create_clubPosting(
    memberPosting_data: MemberPostingSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    memberPosting_data = MemberPosting(
        date=datetime.now(),
        user_seq=token.seq,
        club_seq=memberPosting_data.club_seq,
        title=memberPosting_data.title,
        notice=memberPosting_data.notice,
        status=memberPosting_data.status,
    )
    db.add(memberPosting_data)
    db.commit()

    join_memberPosting_data = JoinMemberPosting(
        member_posting_seq=memberPosting_data.seq,
        club_seq=memberPosting_data.club_seq,
        user_seq=token.seq,
        accepted=False,
    )
    db.add(join_memberPosting_data)
    db.commit()

    return {"success": True}


@memberPosting_router.get("/{member_posting_seq}")
def get_memberPosting(
    token: Annotated[str, Depends(get_current_user)],
    member_posting_seq: int,
    db: Session = Depends(get_db),
):
    member_posting = (
        db.query(MemberPosting)
        .filter(MemberPosting.seq == member_posting_seq)
        .options(joinedload(MemberPosting.user_profile))
        .first()
    )

    # if member_posting is None:
    #     raise MemberPostingNotFoundException

    return member_posting


@memberPosting_router.patch("/{member_posting_seq}")
def update_memberPosting(
    token: Annotated[str, Depends(get_current_user)],
    member_posting_seq: int,
    update_club_posting_data: UpdateMemberPostingSchema,
    db: Session = Depends(get_db),
):
    member_posting = (
        db.query(MemberPosting).filter(MemberPosting.seq == member_posting_seq).first()
    )

    # if not member_posting:
    #     raise MemberPostingNotFoundException

    for key, value in update_club_posting_data.dict(exclude_none=True).items():
        setattr(member_posting, key, value)

    db.commit()

    return {"success": True}


@memberPosting_router.get("")
def filter_memberPosting(
    token: Annotated[str, Depends(get_current_user)],
    member_posting_filter: FilterMemberPostingSchema = FilterDepends(
        FilterMemberPostingSchema
    ),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(MemberPosting)
    query = member_posting_filter.filter(query).options(
        joinedload(MemberPosting.user_profile)
    )
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    member_posting = query.all()

    return member_posting


@memberPosting_router.delete("/{member_posting_seq}")
def delete_clubPosting(
    token: Annotated[str, Depends(get_current_user)],
    member_posting_seq: int,
    db: Session = Depends(get_db),
):
    member_posting = (
        db.query(MemberPosting).filter(MemberPosting.seq == member_posting_seq).first()
    )

    # if not memberPosting:
    #     raise memberPostingNotFoundException

    db.delete(member_posting)
    db.commit()

    return {"message": "매치게시글이 성공적으로 삭제되었습니다."}
