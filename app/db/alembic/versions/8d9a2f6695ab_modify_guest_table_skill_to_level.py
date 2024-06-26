"""modify guest table skill to level

Revision ID: 8d9a2f6695ab
Revises: 240f608b8121
Create Date: 2024-06-22 17:37:16.259090

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8d9a2f6695ab"
down_revision: Union[str, None] = "240f608b8121"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "guest",
        sa.Column("gender", sa.String(12), comment="성별"),
    )
    op.add_column(
        "guest",
        sa.Column("level", sa.Integer, comment="레벨"),
    )
    op.drop_column("guest", "skill")


def downgrade() -> None:
    op.drop_column("guest", "gender")
    op.drop_column("guest", "level")
    op.add_column(
        "guest",
        sa.Column("skill", sa.String(24), comment="실력"),
    )
