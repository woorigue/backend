"""rename user table age to birth date

Revision ID: 6e01656e5ff1
Revises: a070c6bdead6
Create Date: 2024-04-21 09:22:28.479320

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6e01656e5ff1"
down_revision: str | None = "a070c6bdead6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("profile", "age", new_column_name="birth_date")


def downgrade() -> None:
    op.alter_column("profile", "birth_date", new_column_name="age")
