from fastapi import status


class RestException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    user_message: str | None = None
    system_code: str | None = None
    system_message: str | None = None

    def __init__(
        self,
        status_code: int | None = None,
        user_message: str | None = None,
        system_code: str | None = None,
        system_message: str | None = None,
    ) -> None:
        self.status_code = status_code or self.status_code
        self.user_message = user_message or self.user_message
        self.system_code = system_code or self.system_code
        self.system_message = system_message or self.system_message


class ProfileRequired(RestException):
    status = status.HTTP_400_BAD_REQUEST
    user_message = "프로필 설정이 필요합니다."
    system_code = "USER_PROFILE_DATA_REQUIRED"
    system_message = "Profile data is reuqired of user"
