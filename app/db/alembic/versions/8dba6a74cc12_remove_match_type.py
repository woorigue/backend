"""remove match type

Revision ID: 8dba6a74cc12
Revises: 90bbed41cff2
Create Date: 2024-06-19 01:21:59.809868

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8dba6a74cc12"
down_revision: str | None = "90bbed41cff2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("match", "match_type")


def downgrade() -> None:
    pass
