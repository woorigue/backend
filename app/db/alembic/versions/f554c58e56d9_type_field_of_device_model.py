"""type field of device model

Revision ID: f554c58e56d9
Revises: e00f5e1b4782
Create Date: 2024-10-30 00:50:09.268343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.model.device import DeviceTypeEnum


# revision identifiers, used by Alembic.
revision: str = "f554c58e56d9"
down_revision: Union[str, None] = "e00f5e1b4782"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    device_type_enum = sa.Enum(DeviceTypeEnum, name="devicetypeenum")
    device_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "device",
        sa.Column("type", device_type_enum, nullable=True, comment="타입"),
    )


def downgrade() -> None:
    op.drop_column("device", "type")
    sa.Enum(name="devicetypeenum").drop(op.get_bind())
