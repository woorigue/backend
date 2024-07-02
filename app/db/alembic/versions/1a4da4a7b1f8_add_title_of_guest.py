"""add title of guest

Revision ID: 1a4da4a7b1f8
Revises: c957708201aa
Create Date: 2024-07-02 21:47:27.509841

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1a4da4a7b1f8"
down_revision: str | None = "c957708201aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "guest",
        sa.Column("title", sa.String(128), server_default=""),
    )


def downgrade() -> None:
    pass
