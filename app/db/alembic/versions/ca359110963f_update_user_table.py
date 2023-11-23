"""update_user_table

Revision ID: ca359110963f
Revises: 7a6e4a980c35
Create Date: 2023-11-21 23:27:55.064529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ca359110963f"
down_revision: Union[str, None] = "7a6e4a980c35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("clubs", sa.ARRAY(sa.Integer), nullable=True, comment="클럽"),
    )


def downgrade() -> None:
    op.drop_column("users", "clubs")
