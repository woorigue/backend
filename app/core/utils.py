import json
import os

from sqlalchemy.types import ARRAY, TEXT, Integer, TypeDecorator


class JSONEncodedList(TypeDecorator):
    """불변 구조를 JSON 인코딩된 문자열로 나타냅니다."""

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


# 환경 변수에 따라 다른 타입 사용
def get_position_type():
    if os.getenv("TEST_ENV"):
        return JSONEncodedList
    return ARRAY(Integer)
