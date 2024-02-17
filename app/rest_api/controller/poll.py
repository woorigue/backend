from app.model.user import User
from app.model.match import Match
from app.model.poll import Poll, JoinPoll

from sqlalchemy.orm import Session
from app.helper.exception import MatchNotFoundException, PollNotFoundException


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
        self._validate_process(match_seq, self.db)

        poll = Poll(match_seq=match_seq, expired_at=expired_at, user_seq=self.user.seq)
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
