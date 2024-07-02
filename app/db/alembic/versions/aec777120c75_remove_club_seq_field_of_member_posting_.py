"""remove club seq field of member posting table

Revision ID: aec777120c75
Revises: f18694640ef1
Create Date: 2024-07-02 23:24:21.475113

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aec777120c75"
down_revision: str | None = "f18694640ef1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("memberPosting", "club_seq")


def downgrade() -> None:
    pass
