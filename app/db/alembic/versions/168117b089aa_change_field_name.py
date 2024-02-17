"""change field name

Revision ID: 168117b089aa
Revises: 1584b05f8ca9
Create Date: 2024-02-18 00:55:20.924369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "168117b089aa"
down_revision: Union[str, None] = "1584b05f8ca9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("clubPosting", "intro", new_column_name="notice")


def downgrade() -> None:
    op.alter_column("clubPosting", "notice", new_column_name="intro")
