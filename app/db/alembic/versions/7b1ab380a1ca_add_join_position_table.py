"""add join position table

Revision ID: 7b1ab380a1ca
Revises: 9f72e917d4b9
Create Date: 2023-09-07 02:21:10.772035

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7b1ab380a1ca"
down_revision: Union[str, None] = "9f72e917d4b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "join_position",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("position_seq", sa.Integer),
        sa.Column("profile_seq", sa.Integer),
    )


def downgrade() -> None:
    op.drop_table("join_position")
