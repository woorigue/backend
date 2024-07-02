"""change to level field

Revision ID: f18694640ef1
Revises: 1a4da4a7b1f8
Create Date: 2024-07-02 23:07:14.464722

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f18694640ef1"
down_revision: str | None = "1a4da4a7b1f8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("clubPosting", "skill", new_column_name="level")


def downgrade() -> None:
    pass
