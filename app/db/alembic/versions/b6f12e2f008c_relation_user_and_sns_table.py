"""relation user and sns table

Revision ID: b6f12e2f008c
Revises: 3fbe5e20d8da
Create Date: 2023-11-11 01:27:05.258927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6f12e2f008c"
down_revision: Union[str, None] = "3fbe5e20d8da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "sns_user_fk",
        source_table="sns",
        referent_table="users",
        local_cols=["user_seq"],
        remote_cols=["seq"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("sns_user_fk", table_name="sns")
