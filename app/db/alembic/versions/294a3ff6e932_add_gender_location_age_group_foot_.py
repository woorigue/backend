"""add gender location age_group foot column in profile table

Revision ID: 294a3ff6e932
Revises: 445d95b3fb61
Create Date: 2024-02-04 23:54:10.566607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "294a3ff6e932"
down_revision: Union[str, None] = "445d95b3fb61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("profile", "sex", new_column_name="gender")
    op.add_column(
        "profile",
        sa.Column("location", sa.String(24), comment="활동 장소"),
    )
    op.add_column(
        "profile",
        sa.Column("age_group", sa.String(24), comment="연령대"),
    )
    op.add_column(
        "profile",
        sa.Column("foot", sa.String(12), comment="주발"),
    )


def downgrade() -> None:
    op.alter_column("profile", "gender", new_column_name="sex")
    op.drop_column("profile", "location")
    op.drop_column("profile", "age_group")
    op.drop_column("profile", "foot")
