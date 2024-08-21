from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.model.guest import Guest
from app.model.match import Match
from app.rest_api.schema.guest.guest import GuestSchema


class GuestController:
    def register_guest(self, guest_data: GuestSchema, db: Session) -> None:
        ("----guest_data---", guest_data)
        Guest.create(guest_data, db)

    def build_filters(self, filters):
        conditions = []

        filter_map = {
            "seq__in": lambda: Guest.seq.in_(filters.get("seq__in")),
            "user_seq__in": lambda: Guest.user_seq.in_(filters.get("user_seq__in")),
            "club_seq__in": lambda: Guest.club_seq.in_(filters.get("club_seq__in")),
            "match_seq__in": lambda: Guest.match_seq.in_(filters.get("match_seq__in")),
            "level__in": lambda: Guest.level.in_(filters.get("level__in")),
            "gender__in": lambda: Guest.gender.in_(filters.get("gender__in")),
            "position__in": lambda: or_(
                Guest.position.any(pos) for pos in filters.get("position__in")
            ),
            "match_date": lambda: Match.match_date == filters.get("match_date"),
            "match_date__gte": lambda: Match.match_date
            >= filters.get("match_date__gte"),
            "match_date__lte": lambda: Match.match_date
            <= filters.get("match_date__lte"),
            "location__ilike": lambda: Match.location.ilike(
                f"%{filters.get('location__ilike')}%"
            ),
        }

        for key, value in filters.items():
            if value is not None and key in filter_map:
                condition = filter_map[key]()
                if condition is not None:
                    conditions.append(condition)

        return and_(*conditions) if conditions else None


guest_controller = GuestController()
