"""modify_club_table

Revision ID: ddbd6b831a6b
Revises: b6f12e2f008c
Create Date: 2023-11-29 23:44:30.345829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ddbd6b831a6b"
down_revision: Union[str, None] = "b6f12e2f008c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clubs", sa.Column("edit_date", sa.Date, comment="수정일"))
    op.alter_column("clubs", "color", new_column_name="uniform_color")


def downgrade() -> None:
    op.drop_column("clubs", "edit_date")
    op.alter_column("clubs", "uniform_color", new_column_name="color")
