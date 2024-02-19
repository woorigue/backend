"""change age group field of profile

Revision ID: cc26fb5def4e
Revises: 77d0de6ef256
Create Date: 2024-02-13 01:42:44.873923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc26fb5def4e"
down_revision: Union[str, None] = "77d0de6ef256"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("profile", "age_group", new_column_name="age")


def downgrade() -> None:
    op.alter_column("profile", "age", new_column_name="age_group")
