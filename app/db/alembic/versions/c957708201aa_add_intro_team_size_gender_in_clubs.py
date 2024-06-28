"""add intro, team_size, gender in clubs

Revision ID: c957708201aa
Revises: cf9a7a103dc2
Create Date: 2024-06-28 00:09:49.767486

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c957708201aa"
down_revision: Union[str, None] = "cf9a7a103dc2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "clubs",
        sa.Column("intro", sa.String(512), comment="소개글"),
    )
    op.add_column(
        "clubs",
        sa.Column("team_size", sa.Integer, comment="클럽 인원"),
    )
    op.add_column(
        "clubs",
        sa.Column("gender", sa.String(12), comment="성별"),
    )


def downgrade() -> None:
    op.drop_column("clubs", "intro")
    op.drop_column("clubs", "team_size")
    op.drop_column("clubs", "gender")
