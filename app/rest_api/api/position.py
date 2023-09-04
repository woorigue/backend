from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.model.position import Position

position_router = APIRouter(tags=["position"], prefix="/position")


@position_router.get("")
def get_positions(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    return positions
