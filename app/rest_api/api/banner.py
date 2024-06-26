from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user
from app.core.utils import error_responses
from app.helper.exception import BannerNotFoundException
from app.model.banner import Banner
from app.rest_api.controller.file import file_controller as file_con
from app.rest_api.schema.base import CreateResponse

banner_router = APIRouter(tags=["banner"], prefix="/banner")


@banner_router.get("", summary="배너 조회")
def list_banners(db: Session = Depends(get_db)):
    banners = db.query(Banner).order_by(Banner.create_date.desc()).all()
    return banners


@banner_router.get(
    "/{banner_id}",
    summary="배너 상세 조회",
    responses={404: {"description": error_responses([BannerNotFoundException])}},
)
def get_banner(banner_id: int, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.seq == banner_id).first()
    if banner is None:
        raise BannerNotFoundException
    return banner


@banner_router.post(
    "",
    summary="배너 등록",
    response_model=CreateResponse,
)
async def add_banner(
    banner_img: UploadFile,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    banner_content = await banner_img.read()
    file_con.upload_banner_img(banner_content, banner_img.filename, db)
    return {"success": True}


@banner_router.patch(
    "/{banner_id}",
    summary="배너 수정",
    responses={404: {"description": error_responses([BannerNotFoundException])}},
    response_model=CreateResponse,
)
async def edit_banner(
    banner_id: int,
    banner_img: UploadFile,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    banner = db.query(Banner).filter(Banner.seq == banner_id).first()
    if not banner:
        raise BannerNotFoundException

    banner_content = await banner_img.read()
    new_url = file_con.edit_banner_img(banner_content, banner_img.filename)

    banner.url = new_url

    db.commit()
    return {"success": True}


@banner_router.delete(
    "/{banner_id}",
    summary="배너 삭제",
    responses={404: {"description": error_responses([BannerNotFoundException])}},
    response_model=CreateResponse,
)
def delete_banner(
    banner_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    banner = db.query(Banner).filter(Banner.seq == banner_id).first()
    if not banner:
        raise BannerNotFoundException

    db.delete(banner)
    db.commit()
    return {"message": "배너가 성공적으로 삭제되었습니다."}
