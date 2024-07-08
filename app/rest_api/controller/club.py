from app.model.club import Club, JoinClub
from app.model.user import User

from sqlalchemy.orm import Session


class ClubController:
    """클럽 컨트롤러"""

    def __init__(self, user: User) -> None:
        self.user = user

    def is_owner(self, db: Session, club_seq: int) -> bool:
        """클럽 소유주 여부를 체크하는 함수"""
        from sqlalchemy.sql import exists

        return db.query(
            exists().where(
                JoinClub.role == "owner",
                JoinClub.user_seq == self.user.seq,
                JoinClub.clubs_seq == club_seq,
            )
        ).scalar()

    def get_joined_member(self, db: Session, club_seq: int) -> int:
        return db.query(Club).filter(Club.seq == club_seq).join(Club.members).count()
