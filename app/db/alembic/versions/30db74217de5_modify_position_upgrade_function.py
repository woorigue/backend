"""modify position upgrade function

Revision ID: 30db74217de5
Revises: d35415c31651
Create Date: 2023-11-18 20:46:01.920281

"""
from typing import Sequence, Union

from alembic import op

# import sqlalchemy as sa
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision: str = "30db74217de5"
down_revision: Union[str, None] = "d35415c31651"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    data = [
        {"seq": 1, "name": "GK"},
        {"seq": 2, "name": "RB"},
        {"seq": 3, "name": "RWB"},
        {"seq": 4, "name": "CB"},
        {"seq": 5, "name": "LB"},
        {"seq": 6, "name": "LWB"},
        {"seq": 7, "name": "CDM"},
        {"seq": 8, "name": "RM"},
        {"seq": 9, "name": "CM"},
        {"seq": 10, "name": "LM"},
        {"seq": 11, "name": "CAM"},
        {"seq": 12, "name": "RW"},
        {"seq": 13, "name": "ST"},
        {"seq": 14, "name": "LW"},
        {"seq": 15, "name": "CF"},
    ]

    metadata = MetaData()
    position_table = Table("position", metadata, autoload_with=op.get_bind())
    op.bulk_insert(position_table, data)


def downgrade() -> None:
    pass
