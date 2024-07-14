from enum import IntEnum, StrEnum


#################
### Club Enum ###
#################
class GenderEnum(StrEnum):
    """성별 열거형 클래스"""

    FEMAIL = "F"
    MAIL = "M"
    UNISEX = "U"


class LevelEnum(IntEnum):
    """클럽 실력"""

    BEGINNER = 1  # 입문
    INTERMEDIATE = 2  # 중급
    ADVANCED = 3  # 고급
    EXPERT = 4  # 전문가
    ELITE = 5  # 엘리트
