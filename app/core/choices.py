from enum import Enum


class PostingStatusEnum(str, Enum):
    PUBLISHED = "published"
    CLOSED = "closed"
