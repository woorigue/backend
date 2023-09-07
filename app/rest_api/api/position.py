from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.model.position import Position
from app.rest_api.schema.position import PositionSchema

position_router = APIRouter(tags=["position"], prefix="/position")


@position_router.get("", response_model=PositionSchema)
def get_positions(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    return positions
