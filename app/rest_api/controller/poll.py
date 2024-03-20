from app.model.user import User
from app.model.match import Match
from app.model.poll import Poll, JoinPoll
from app.model.club import JoinClub

from sqlalchemy.orm import Session
from app.helper.exception import (
    MatchNotFoundException,
    PollNotFoundException,
    JoinClubNotFoundException,
)


class PollValidator:
    """validator class of poll"""

    def _validate_process(self, match_seq: int, db: Session):
        # validate match object
        match = db.query(Match).filter(Match.seq == match_seq).first()

        if not match:
            raise MatchNotFoundException

        # TODO: validate club owner


class PollController(PollValidator):
    """controller class of poll"""

    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

    def create_poll(self, data):
        expired_at = data.expired_at
        match_seq = data.match_seq
        club_seq = data.club_seq
        self._validate_process(match_seq, self.db)

        poll = Poll(
            match_seq=match_seq,
            expired_at=expired_at,
            user_seq=self.user.seq,
            club_seq=club_seq,
        )
        self.db.add(poll)
        self.db.commit()

    def retrieve_poll(self, poll_id: int):
        poll = self.db.query(Poll).filter(Poll.seq == poll_id).first()

        if not poll:
            raise PollNotFoundException

        return poll

    def update_poll(self, poll_id: int, data):
        poll = (
            self.db.query(Poll)
            .filter(Poll.seq == poll_id, Poll.user_seq == self.user.seq)
            .first()
        )

        if not poll:
            raise PollNotFoundException

        self.db.query(Poll).filter(
            Poll.seq == poll_id, Poll.user_seq == self.user.seq
        ).update({"expired_at": data.expired_at, "vote_closed": data.vote_closed})
        self.db.commit()
        self.db.flush()

    def delete_poll(self, poll_id: int):
        poll = (
            self.db.query(Poll)
            .filter(Poll.seq == poll_id, Poll.user_seq == self.user.seq)
            .first()
        )

        if not poll:
            raise PollNotFoundException

        self.db.delete(poll)
        self.db.commit()

    def join_poll(self, poll_id: int):
        poll = self.db.query(Poll).filter(Poll.seq == poll_id).first()

        if not poll:
            raise PollNotFoundException

        join_club = (
            self.db.query(JoinClub)
            .filter(
                JoinClub.clubs_seq == poll.club_seq, JoinClub.user_seq == self.user.seq
            )
            .first()
        )

        if not join_club:
            raise JoinClubNotFoundException

        join_poll = JoinPoll(attend=True, user_seq=self.user.seq, poll_seq=poll.seq)
        self.db.add(join_poll)
        self.db.commit()
