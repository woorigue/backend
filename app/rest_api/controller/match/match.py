from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.club import JoinClub
from app.rest_api.schema.match.match import MatchSchema


class MatchController:
    def __init__(self, db: Session):
        self.db = db

    def validate_match_register(self, match_data: MatchSchema, user_seq: int) -> bool:
        # 내가 소속된 클럽인지 확인하는 로직
        join_club = self.db.scalar(
            select(JoinClub).where(
                JoinClub.user_seq == user_seq,
                JoinClub.clubs_seq == match_data.home_club_seq,
            )
        )
        return join_club
