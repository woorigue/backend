"""modify club skill to level

Revision ID: 9d552ce94878
Revises: 58d44d965ece
Create Date: 2024-06-02 17:58:15.592819

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9d552ce94878"
down_revision: Union[str, None] = "58d44d965ece"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "clubs",
        sa.Column("level", sa.Integer, comment="레벨"),
    )
    op.drop_column("clubs", "skill")


def downgrade() -> None:
    op.drop_column("clubs", "level")
    op.add_column(
        "clubs",
        sa.Column("skill", sa.String(24), comment="실력"),
    )
