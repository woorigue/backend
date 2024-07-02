from fastapi import HTTPException, status


class RestException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: int = 999999
    error_detail: str = ""

    def __init__(
        self,
        status_code: int | None = None,
        error_code: str | None = None,
        error_detail: str | None = None,
    ) -> None:
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.error_detail = error_detail or self.error_detail


class ProfileRequired(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100000
    error_detail = "프로필 설정이 필요합니다"


class EmailConflictException(RestException):
    status_code = status.HTTP_409_CONFLICT
    error_code = 100001
    error_detail = "이메일 중복 오류 발생"


class EmailExpiredException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100002
    error_detail = "인증이 만료되었습니다.다시 시도해주세요."


class EmailAuthNumberInvalidException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100003
    error_detail = "인증번호가 맞지 않습니다.다시 확인해주세요."


class PasswordInvalidException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100003
    error_detail = "비밀번호 최소 길이는 6자입니다."


class UserNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100004
    error_detail = "사용자 정보를 찾을 수 없습니다."


class UserRetrieveFailException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100005
    error_detail = "사용자 정보를 조회하는데 실패했습니다."


class UserPasswordNotMatchException(RestException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = 100006
    error_detail = "비밀번호가 틀렸습니다."


class BannerNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100007
    error_detail = "배너가 존재하지 않습니다."


class FaqNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100008
    error_detail = "질문게시글이 존재하지 않습니다."


class ClubNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100008
    error_detail = "클럽이 존재하지 않습니다."


class JoinClubNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100009
    error_detail = "해당 클럽에 소속되어 있지 않습니다."


class MatchNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100010
    error_detail = "매치글이 존재하지 않습니다."


class JoinMatchNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100011
    error_detail = "매치 신청이 존재하지 않습니다."


class GuestNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100012
    error_detail = "용병글이 존재하지 않습니다."


class JoinGuestNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100013
    error_detail = "용병 신청이 존재하지 않습니다."


class PollNotFoundException(RestException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 100014
    error_detail = "투표가 존재하지 않습니다"


class SnsRequired(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100016
    error_detail = "SNS 로그인이 필요합니다."


class NotFoudnJoinClub(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100017
    error_detail = "소속된 클럽 정보가 존재하지 않습니다"


class RegisterMatchError(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100018
    error_detail = "매칭을 생성하는데 실패하였습니다"


class JoinClubLimitError(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100019
    error_detail = "클럽에 참여할 수 있는 팀은 최대 2팀 입니다."


class GuestPermissionDeniedException(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100020
    error_detail = "해당 게시글을 수정할 수 있는 권한이 없습니다."


class ClubPostingCreatePermissionDenied(RestException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 100021
    error_detail = "해당 클럽의 모집공고를 작성할 수 있는 권한이 없습니다."
