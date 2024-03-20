"""remove age, gender, skill, location field in MemberPosting table

Revision ID: 0e8b215b1c84
Revises: 7421372e6015
Create Date: 2024-02-22 20:09:36.208514

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e8b215b1c84"
down_revision: Union[str, None] = "7421372e6015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("memberPosting", "age_group")
    op.drop_column("memberPosting", "gender")
    op.drop_column("memberPosting", "skill")
    op.drop_column("memberPosting", "location")
    op.drop_column("memberPosting", "membership_fee")
    op.alter_column("memberPosting", "intro", new_column_name="notice")


def downgrade() -> None:
    op.add_column(
        "memberPosting",
        sa.Column("age_group", sa.String(24), comment="연령대"),
    )
    op.add_column(
        "memberPosting",
        sa.Column("gender", sa.String(12), comment="성별"),
    )
    op.add_column(
        "memberPosting",
        sa.Column("skill", sa.String(24), comment="실력"),
    )
    op.add_column(
        "memberPosting",
        sa.Column("location", sa.String(24), comment="활동 장소"),
    )
    op.add_column(
        "memberPosting",
        sa.Column("membership_fee", sa.Integer, comment="회비"),
    )
    op.alter_column("memberPosting", "notice", new_column_name="intro")
