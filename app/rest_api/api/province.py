from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db

province_router = APIRouter(tags=["province"], prefix="/province")


@province_router.get("", deprecated=True)
def get_provinces(db: Session = Depends(get_db)):
    return {"success": True}
