"""add position model

Revision ID: 9f72e917d4b9
Revises: 92944486d621
Create Date: 2023-09-05 01:06:43.652680

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f72e917d4b9"
down_revision: Union[str, None] = "92944486d621"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "position",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("name", sa.String(12), comment="이름"),
    )


def downgrade() -> None:
    op.drop_table("position")
