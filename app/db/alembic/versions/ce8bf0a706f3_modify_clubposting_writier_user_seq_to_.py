"""modify clubPosting writier_user_seq to user_seq

Revision ID: ce8bf0a706f3
Revises: 9595a3280bd6
Create Date: 2024-02-19 00:46:19.771796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ce8bf0a706f3"
down_revision: Union[str, None] = "9595a3280bd6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    print("HERE")


def downgrade() -> None:
    op.alter_column("clubPosting", "user_seq", new_column_name="writer_user_seq")
