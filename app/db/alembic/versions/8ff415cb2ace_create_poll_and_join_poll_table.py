"""create poll and join poll table

Revision ID: 8ff415cb2ace
Revises: 702f43f1b165
Create Date: 2024-01-28 21:54:18.139623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8ff415cb2ace"
down_revision: Union[str, None] = "1928da62cee6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "poll",
        sa.Column("seq", sa.Integer, autoincrement=True, nullable=False, comment="시퀀스"),
        sa.Column("expired_at", sa.DateTime, nullable=True, comment="투표 종료 시간"),
        sa.Column(
            "vote_closed",
            sa.Boolean,
            nullable=True,
            default=False,
            comment="투표 종료 여부",
        ),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=True,
            default=sa.func.utcnow,
            comment="생성 시간",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=True,
            default=sa.func.utcnow,
            comment="수정 시간",
        ),
        sa.Column("match_seq", sa.Integer, nullable=True),
        sa.Column("user_seq", sa.Integer, nullable=True),
        sa.PrimaryKeyConstraint("seq"),
    )
    op.create_table(
        "join_poll",
        sa.Column("seq", sa.Integer, autoincrement=True, nullable=False, comment="시퀀스"),
        sa.Column("attend", sa.Boolean, nullable=True, comment="참석 여부"),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=True,
            default=sa.func.utcnow,
            comment="생성 시간",
        ),
        sa.Column("user_seq", sa.Integer, nullable=True),
        sa.Column("poll_seq", sa.Integer, nullable=True),
    )
    op.create_foreign_key(
        "join_poll_user_fk",
        "join_poll",
        "users",
        ["user_seq"],
        ["seq"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "join_poll_poll_fk",
        "join_poll",
        "poll",
        ["poll_seq"],
        ["seq"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "poll_match_fk",
        "poll",
        "match",
        ["match_seq"],
        ["seq"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "poll_user_fk",
        "poll",
        "users",
        ["user_seq"],
        ["seq"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_table("join_poll")
    op.drop_table("poll")
