"""create_club_table

Revision ID: 1cdfc9d0487f
Revises: 30db74217de5
Create Date: 2023-11-19 18:29:18.529107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1cdfc9d0487f"
down_revision: Union[str, None] = "30db74217de5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clubs",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("name", sa.String(24), comment="클럽명"),
        sa.Column("register_date", sa.Date, comment="창단일"),
        sa.Column("location", sa.String(24), comment="활동 장소"),
        sa.Column("age_group", sa.String(24), comment="연령대"),
        sa.Column("membership_fee", sa.Integer, comment="회비"),
        sa.Column("skill", sa.String(24), comment="실력"),
        sa.Column("img", sa.String(256), comment="클럽 이미지 URL"),
        sa.Column("color", sa.String(24), comment="유니폼 색"),
    )


def downgrade() -> None:
    op.drop_table("clubs")
