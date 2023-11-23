from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.model.banner import Banner

from app.rest_api.controller.file import file_controller as file_con

from app.rest_api.schema.banner import (BannerRegisterSchema, BannerDeleteSchema)

from app.helper.exception import(
    BannerNotFoundException
)


banner_router = APIRouter(tags=["banner"], prefix="/banner")

@banner_router.get("")
def get_banners(db: Session = Depends(get_db)):
    banners = db.query(Banner).order_by(Banner.create_date.desc()).all()
    return banners
    
@banner_router.post("")
async def add_banners(banner_img:UploadFile, db: Session = Depends(get_db)):
    banner_content = await banner_img.read()
    file_con.upload_banner_img(banner_content, banner_img.filename, db)
    return {"success": True}

@banner_router.delete("/{banner_id}")
def delete_banners(banner_id:int, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise BannerNotFoundException
        
    db.delete(banner)
    db.commit()
    return {"message": "배너가 성공적으로 삭제되었습니다."}