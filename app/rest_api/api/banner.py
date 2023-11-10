from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.model.banner import Banner

from app.rest_api.schema.banner import (BannerRegisterSchema, BannerDeleteSchema)

banner_router = APIRouter(tags=["banner"], prefix="/banner")

@banner_router.get("")
def get_banners(db: Session = Depends(get_db)):
    banners = db.query(Banner).all()
    return banners
    
@banner_router.post("")
def add_banners(user_data:BannerRegisterSchema, db: Session = Depends(get_db)):
    new_banner = Banner(url=user_data.url)
    db.add(new_banner)
    db.commit()
    return {"message": "배너가 성공적으로 등록되었습니다.", "banner": new_banner.url}

@banner_router.delete("/{banner_id}")
def delete_banners(banner_id:int, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.id === banner_id).first()
    if not banner:
        return HTTPException(status_code=404, detail="배너가 존재하지 않습니다.")
    db.delete(banner)
    db.commit()
    return {"message": "배너가 성공적으로 삭제되었습니다."}