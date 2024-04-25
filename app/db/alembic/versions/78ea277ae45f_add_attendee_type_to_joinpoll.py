"""add attendee_type to JoinPoll

Revision ID: 78ea277ae45f
Revises: a5c6aaafa619
Create Date: 2024-04-15 22:24:00.605053

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "78ea277ae45f"
down_revision: str | None = "a5c6aaafa619"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "join_poll",
        sa.Column("attendee_type", sa.String(16), comment="참석자 종류"),
    )


def downgrade() -> None:
    op.drop_column("join_poll", "attendee_type")
