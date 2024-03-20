"""create chat

Revision ID: 702f43f1b165
Revises: 50432d531f5c
Create Date: 2024-01-05 15:08:46.248336

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "702f43f1b165"
down_revision: Union[str, None] = "50432d531f5c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create ChattingRoom table first
    op.create_table(
        "chatting_room",
        sa.Column(
            "seq", sa.Integer, primary_key=True, autoincrement=True, comment="시퀀스"
        ),
        sa.Column(
            "created_at",
            sa.DateTime,
            default=sa.func.current_timestamp(),
            nullable=True,
            comment="생성 시간",
        ),
    )

    # Then create UserChatRoomAssociation table
    op.create_table(
        "user_chatroom_association",
        sa.Column("userId", sa.Integer, sa.ForeignKey("users.seq"), primary_key=True),
        sa.Column(
            "chat_room_seq",
            sa.Integer,
            sa.ForeignKey("chatting_room.seq"),
            primary_key=True,
        ),
        sa.Column("joinDate", sa.DateTime, nullable=False, comment="참여 일자"),
    )

    # Finally, create ChattingContent table
    op.create_table(
        "chatting_content",
        sa.Column(
            "seq", sa.Integer, primary_key=True, autoincrement=True, comment="메시지 ID"
        ),
        sa.Column(
            "chatting_room_seq",
            sa.Integer,
            sa.ForeignKey("chatting_room.seq"),
            nullable=False,
            comment="채팅방 ID",
        ),
        sa.Column(
            "user_seq",
            sa.Integer,
            sa.ForeignKey("users.seq"),
            nullable=False,
            comment="사용자 ID",
        ),
        sa.Column("content", sa.Text, nullable=False, comment="메시지 내용"),
        sa.Column(
            "created_at",
            sa.DateTime,
            default=sa.func.current_timestamp(),
            nullable=True,
            comment="생성 시간",
        ),
    )


def downgrade():
    op.drop_table("chatting_content")
    op.drop_table("user_chatroom_association")
    op.drop_table("chatting_room")
