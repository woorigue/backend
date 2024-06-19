"""modify profile birthdate to age

Revision ID: f94d26f2f139
Revises: 8dba6a74cc12
Create Date: 2024-06-19 00:16:51.441261

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f94d26f2f139"
down_revision: Union[str, None] = "8dba6a74cc12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("profile", sa.Column("age", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("profile", "age")
