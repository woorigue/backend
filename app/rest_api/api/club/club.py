from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi_filter import FilterDepends
from sqlalchemy import and_, delete, exists, or_
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_db
from app.core.token import get_current_user
from app.helper.exception import (
    ClubNotFoundException,
    JoinClubLimitError,
    JoinClubNotFoundException,
)
from app.model.club import Club, JoinClub
from app.model.match import Match
from app.model.position import JoinPosition
from app.model.profile import Profile
from app.rest_api.controller.file import file_controller as file_con
from app.rest_api.schema.club.club import (
    ClubResponseSchema,
    FilterClubSchema,
    GetClubMemberSchema,
    UpdateClubSchema,
)
from app.rest_api.schema.profile import GetProfileSchema

club_router = APIRouter(tags=["club"], prefix="/club")


from fastapi import APIRouter


@club_router.post("")
async def create_club(
    token: Annotated[str, Depends(get_current_user)],
    emblem_img: UploadFile | None = File(None),
    img: UploadFile | None = File(None),
    register_date: str = Form(...),
    level: int = Form(...),
    intro: str = Form(...),
    name: str = Form(...),
    location: str = Form(...),
    team_size: int = Form(...),
    gender: str = Form(...),
    uniform_color: str = Form(...),
    membership_fee: int = Form(...),
    age_group: str = Form(...),
    db: Session = Depends(get_db),
):
    # join_club_count = db.query(JoinClub).where(JoinClub.user_seq == token.seq).count()
    # if join_club_count > 2:
    #     raise JoinClubLimitError

    emblem_url = ""
    if emblem_img is not None:
        emblem_contents = await emblem_img.read()
        emblem_url = file_con.upload_club_img(emblem_contents, emblem_img.filename)

    img_url = ""
    if img is not None:
        img_contents = await img.read()
        img_url = file_con.upload_club_img(img_contents, img.filename)

    club = Club(
        name=name,
        register_date=register_date,
        intro=intro,
        location=location,
        age_group=age_group,
        membership_fee=membership_fee,
        level=level,
        team_size=team_size,
        gender=gender,
        emblem_img=emblem_url,
        img=img_url,
        uniform_color=uniform_color,
    )
    db.add(club)
    db.commit()

    join_club = JoinClub(
        clubs_seq=club.seq, user_seq=token.seq, role="owner", accepted=True
    )
    db.add(join_club)
    db.commit()

    return {"success": True}


@club_router.get("/{club_seq}", response_model=ClubResponseSchema)
def get_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    if club is None:
        raise ClubNotFoundException

    return club


@club_router.patch("/{club_seq}")
def update_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    update_club_data: UpdateClubSchema,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    if club is None:
        raise ClubNotFoundException

    for key, value in update_club_data.dict(exclude_none=True).items():
        setattr(club, key, value)

    db.commit()

    return {"success": True}


@club_router.get("", response_model=list[ClubResponseSchema])
def filter_clubs(
    token: Annotated[str, Depends(get_current_user)],
    club_filter: FilterClubSchema = FilterDepends(FilterClubSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Club)
    query = club_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    clubs = query.all()

    return clubs


@club_router.post("/{club_seq}/join")
def join_club(
    club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    join_status = db.query(
        exists().where(
            (JoinClub.user_seq == token.seq) & (JoinClub.clubs_seq == club_seq)
        )
    ).scalar()

    if not join_status:
        join_club = JoinClub(user_seq=token.seq, clubs_seq=club_seq, role="member")
        db.merge(join_club)
        db.commit()
        db.flush()

    return {"success": True}


@club_router.patch("/{club_seq}/accept")
def accept_club(
    club_seq: int,
    user_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()
    if not club:
        raise ClubNotFoundException

    join_club = (
        db.query(JoinClub)
        .filter(
            JoinClub.club_seq == club_seq,
            JoinClub.user_seq == user_seq,
        )
        .one()
    )

    if not join_club:
        raise JoinClubNotFoundException

    # TODO: validate club owner / matcher poster

    join_club.accepted = True

    return {"success": True}


@club_router.delete("/{club_seq}/quit")
def quit_club(
    club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    join_club = delete(JoinClub).where(
        and_(JoinClub.user_seq == token.seq, JoinClub.clubs_seq == club_seq)
    )
    db.execute(join_club)
    db.commit()
    db.flush()

    return {"success": True}


@club_router.delete("/{club_seq}")
def delete_club(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.seq == club_seq).first()

    if club is None:
        raise ClubNotFoundException

    db.delete(club)
    db.commit()

    return {"message": "클럽이 성공적으로 삭제되었습니다."}


@club_router.get(
    "/{club_seq}/members",
    response_model=list[GetClubMemberSchema],
)
def get_members(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    members_query = (
        db.query(Profile, JoinClub.role)
        .join(JoinClub, Profile.user_seq == JoinClub.user_seq)
        .filter(JoinClub.clubs_seq == club_seq, JoinClub.accepted == True)
        .options(joinedload(Profile.join_position).joinedload(JoinPosition.position))
        .all()
    )

    member = [
        GetClubMemberSchema(
            profile=GetProfileSchema.from_orm(member[0]), role=member[1]
        )
        for member in members_query
    ]

    return member


@club_router.get("/{club_seq}/match_schedule")
def get_match_schedule(
    token: Annotated[str, Depends(get_current_user)],
    club_seq: int,
    db: Session = Depends(get_db),
):
    match_scehdule = (
        db.query(Match)
        .filter(or_(Match.home_club_seq == club_seq, Match.away_club_seq == club_seq))
        .all()
    )

    return match_scehdule
