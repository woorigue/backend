from sqlalchemy.orm import Session

from app.model.match import Match
from app.rest_api.schema.match.match import MatchSchema


class MatchController:
    def register_match(self, match_data: MatchSchema, db: Session) -> None:
        Match.create(match_data, db)


match_controller = MatchController()
