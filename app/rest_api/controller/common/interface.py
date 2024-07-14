from abc import ABC, abstractmethod


class PostingInterface(ABC):
    """
    포스팅 추상클래스
    Target:
        팀 회원 모집 공고
        팀 가입 모집 공고
    """

    @abstractmethod
    def validate(self):
        """데이터 유효성 체크"""
        pass

    @abstractmethod
    def update(self):
        """포스팅 수정"""
        pass

    @abstractmethod
    def delete(self):
        """포스팅 삭제"""
        pass

    @abstractmethod
    def is_creator(self):
        pass
