"""create_club_posting_table

Revision ID: d39c4d15bc06
Revises: f12379ae880b
Create Date: 2023-12-26 00:20:06.972153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d39c4d15bc06"
down_revision: Union[str, None] = "f12379ae880b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clubPosting",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("club_seq", sa.Integer, comment="클럽 시퀸스"),
        sa.Column("title", sa.String(128), comment="제목"),
        sa.Column("intro", sa.String(255), comment="클럽 소개글"),
        sa.Column("recruitment_number", sa.Integer, comment="모집 회원 수"),
        sa.Column("location", sa.String(24), comment="활동 장소"),
        sa.Column("age_group", sa.String(24), comment="연령대"),
        sa.Column("membership_fee", sa.Integer, comment="회비"),
        sa.Column("skill", sa.String(24), comment="실력"),
        sa.Column("gender", sa.String(12), comment="성별"),
        sa.Column("status", sa.String(24), comment="상태"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
    )


def downgrade() -> None:
    op.drop_table("clubPosting")
