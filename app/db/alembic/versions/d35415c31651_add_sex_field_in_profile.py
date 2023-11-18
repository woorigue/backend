"""add_sex_field_in_profile

Revision ID: d35415c31651
Revises: 71c407fe216c
Create Date: 2023-11-17 20:33:43.393258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d35415c31651"
down_revision: Union[str, None] = "71c407fe216c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profile",
        sa.Column("sex", sa.String(1), default="M", comment="성별"),
    )


def downgrade() -> None:
    op.drop_column("profile", "sex")
