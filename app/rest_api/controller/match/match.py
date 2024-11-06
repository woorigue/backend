from datetime import datetime
from pytz import timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.club import JoinClub
from app.model.match import Match
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

        # 내가 이미 생성해놓은 매치의 start_time & end_time range를 체크하는 로직
        match = self.db.scalar(
            select(Match).where(
                Match.match_date == match_data.match_date,
                Match.start_time >= match_data.start_time,
                Match.end_time <= match_data.end_time,
            )
        )

        if join_club is not None and match is None:
            return True

        return False

    def validate_match_date(self, match_data: MatchSchema) -> bool:

        kst = timezone("Asia/Seoul")
        now = datetime.now(kst)
        today = now.date()

        if match_data.match_date > today or (
            match_data.match_date == today and match_data.start_time > now.time()
        ):
            return True

        return False
