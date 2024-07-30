"""remove clubs columns in profile table

Revision ID: 255977718c41
Revises: 17c8e176960f
Create Date: 2024-07-27 18:04:32.985927

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "255977718c41"
down_revision: Union[str, None] = "17c8e176960f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "clubs")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("clubs", sa.ARRAY(sa.Integer), nullable=True, comment="클럽"),
    )
