"""remove team_size in club

Revision ID: 17c8e176960f
Revises: bac45f0b964a
Create Date: 2024-07-10 22:06:10.004923

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "17c8e176960f"
down_revision: Union[str, None] = "bac45f0b964a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("clubs", "team_size")


def downgrade() -> None:
    op.add_column(
        "clubs",
        sa.Column("team_size", sa.Integer, comment="클럽 인원"),
    )
