"""add position field in profile

Revision ID: 92944486d621
Revises: 75a7ada463d9
Create Date: 2023-09-03 11:09:32.210828

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "92944486d621"
down_revision: Union[str, None] = "75a7ada463d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profile",
        sa.Column("positions", sa.ARRAY(sa.Integer), nullable=True, comment="포지션"),
    )


def downgrade() -> None:
    op.drop_column("profile", "positions")
