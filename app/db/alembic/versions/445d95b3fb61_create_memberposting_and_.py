"""create memberPosting and JoinMemberPosting table

Revision ID: 445d95b3fb61
Revises: 75ec3808e380
Create Date: 2024-02-04 23:05:08.683360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "445d95b3fb61"
down_revision: Union[str, None] = "4233de6985fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "memberPosting",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
        sa.Column("club_seq", sa.Integer, comment="클럽 시퀸스"),
        sa.Column("title", sa.String(128), comment="제목"),
        sa.Column("intro", sa.String(255), comment="클럽 소개글"),
        sa.Column("age_group", sa.String(24), comment="연령대"),
        sa.Column("gender", sa.String(12), comment="성별"),
        sa.Column("skill", sa.String(24), comment="실력"),
        sa.Column("location", sa.String(24), comment="활동 장소"),
        sa.Column("membership_fee", sa.Integer, comment="회비"),
        sa.Column("status", sa.String(24), comment="상태"),
    )

    op.create_table(
        "join_memberPosting",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("member_posting_seq", sa.Integer, comment="멤버 포스팅 시퀸스"),
        sa.Column("club_seq", sa.Integer, comment="클럽 시퀸스"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
        sa.Column("accepted", sa.Boolean, comment="수락 여부"),
    )


def downgrade() -> None:
    op.drop_table("memberPosting")
    op.drop_table("join_memberPosting")
