"""relation table profile

Revision ID: 75a7ada463d9
Revises: be01e375b6d9
Create Date: 2023-09-03 02:41:36.363927

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "75a7ada463d9"
down_revision: Union[str, None] = "be01e375b6d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "profile_user_fk",
        source_table="profile",
        referent_table="users",
        local_cols=["user_seq"],
        remote_cols=["seq"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("profile_user_fk", table_name="profile")
