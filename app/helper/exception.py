from fastapi import status
from app.constants.errors import (
    EMAIL_VERIFY_CODE_EXPIRED_SYSTEM_CODE,
    EMAIL_AUTH_NUMBER_INVALID_SYSTEM_CODE,
    PASSWORD_INVALID_SYSTEM_CODE,
    USER_NOT_FOUND_SYSTEM_CODE,
    BANNER_NOT_FOUND_SYSTEM_CODE
)


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
    status_code = status.HTTP_400_BAD_REQUEST
    user_message = "프로필 설정이 필요합니다."
    system_code = "USER_PROFILE_DATA_REQUIRED"
    system_message = "User's Profile data is reuqired"


class EmailConflictException(RestException):
    status_code = status.HTTP_409_CONFLICT
    user_message = "이미 사용중인 이메일입니다."
    system_code = "EMAIL_ALREADY_EXISTS"
    system_message = "Email is already in use"


class EmailExpiredException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    user_message = "인증이 만료되었습니다.다시 시도해주세요."
    system_code = EMAIL_VERIFY_CODE_EXPIRED_SYSTEM_CODE
    system_message = "Verify code has expired"


class EmailAuthNumberInvalidException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    user_message = "인증번호가 맞지 않습니다.다시 확인해주세요."
    system_code = EMAIL_AUTH_NUMBER_INVALID_SYSTEM_CODE
    system_message = "Auth number is not matched"


class PasswordInvalidException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    user_message = "비밀번호 최소 길이는 6자입니다."
    system_code = PASSWORD_INVALID_SYSTEM_CODE
    system_message = "Password need at least 6 characters"


class UserNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    user_message = "사용자 정보를 찾을 수 없습니다."
    system_code = USER_NOT_FOUND_SYSTEM_CODE
    system_message = "User(email) not found"


class UserPasswordNotMatchException(RestException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    user_message = "비밀번호가 틀렸습니다."
    system_code = PASSWORD_INVALID_SYSTEM_CODE
    system_message = "User's password is not matched"
    

class BannerNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    user_message = "배너가 존재하지 않습니다."
    system_code = BANNER_NOT_FOUND_SYSTEM_CODE
    system_message = "Banner not found"    
