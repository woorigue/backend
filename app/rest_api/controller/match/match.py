from sqlalchemy.orm import Session

from app.model.match import Match
from app.rest_api.schema.match.match import MatchRegisterSchema


class MatchController:
    def register_match(self, match_data: MatchRegisterSchema, db: Session) -> None:
        Match.create(match_data, db)


match_controller = MatchController()
