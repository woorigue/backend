from sqlalchemy import exists, func
from sqlalchemy.orm import Session

from app.helper.exception import (
    JoinClubNotFoundException,
    MatchNotFoundException,
    PollNotFoundException,
    PollExpiredException,
)
from pytz import timezone
from app.model.club import JoinClub
from app.model.match import Match
from app.model.poll import JoinPoll, Poll
from app.model.user import User
from datetime import datetime, timedelta


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

        return poll

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

    def join_poll(self, poll_id: int, attend: bool):
        poll = self.db.query(Poll).filter(Poll.seq == poll_id).first()

        if not poll:
            raise PollNotFoundException

        join_club = (
            self.db.query(JoinClub)
            .filter(
                JoinClub.clubs_seq == poll.club_seq,
                JoinClub.user_seq == self.user.seq,
                JoinClub.accepted == True,
            )
            .first()
        )

        if not join_club:
            raise JoinClubNotFoundException

        user_has_voted = self.db.query(
            exists().where(
                (JoinPoll.user_seq == self.user.seq) & (JoinPoll.poll_seq == poll.seq)
            )
        ).scalar()

        kst = timezone("Asia/Seoul")
        match_end_time = (
            poll.match.match_date
            + timedelta(
                hours=poll.match.end_time.hour, minutes=poll.match.end_time.minute
            )
        ).astimezone(kst)
        now = datetime.now(kst)

        if now > match_end_time:
            raise PollExpiredException

        if user_has_voted:
            join_poll = (
                self.db.query(JoinPoll)
                .filter(
                    JoinPoll.user_seq == self.user.seq,
                    JoinPoll.poll_seq == poll.seq,
                )
                .one()
            )
            join_poll.attend = attend
        else:
            join_poll = JoinPoll(
                attend=attend,
                user_seq=self.user.seq,
                poll_seq=poll.seq,
                attendee_type="member",
            )

        self.db.merge(join_poll)
        self.db.commit()

    def poll_status(self, poll_id: int):
        poll = self.db.query(Poll).filter(Poll.seq == poll_id).first()

        if not poll:
            raise PollNotFoundException

        poll_status = (
            self.db.query(
                JoinPoll.attend, JoinPoll.attendee_type, func.count().label("count")
            )
            .filter(JoinPoll.poll_seq == poll_id)
            .group_by(JoinPoll.attend, JoinPoll.attendee_type)
            .all()
        )

        poll_status_list = [
            {"attend": attend, "attendee_type": attendee_type, "count": count}
            for attend, attendee_type, count in poll_status
        ]

        return poll_status_list
