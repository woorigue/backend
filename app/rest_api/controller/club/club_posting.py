from app.model.user import User
from app.rest_api.controller.common.interface import PostingInterface


class ClubPostingController(PostingInterface):
    def __init__(self, user: User) -> None:
        self.user = user

    def validate(self) -> bool:
        pass

    def update(self) -> None:
        pass

    def delete(self) -> None:
        pass

    def is_creator(self) -> bool:
        pass
