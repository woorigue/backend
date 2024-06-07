"""modify match skill to level

Revision ID: 90bbed41cff2
Revises: 9d552ce94878
Create Date: 2024-06-04 21:53:10.471221

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "90bbed41cff2"
down_revision: Union[str, None] = "9d552ce94878"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column("level", sa.Integer, comment="레벨"),
    )
    op.drop_column("match", "skill")


def downgrade() -> None:
    op.drop_column("match", "level")
    op.add_column(
        "match",
        sa.Column("skill", sa.String(24), comment="실력"),
    )
