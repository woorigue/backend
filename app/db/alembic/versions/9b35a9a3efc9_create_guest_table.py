"""create_guest_table

Revision ID: 9b35a9a3efc9
Revises: 9a2e4c883b1d
Create Date: 2023-12-27 20:25:22.858488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision: str = '9b35a9a3efc9'
down_revision: Union[str, None] = '9a2e4c883b1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
     "guest",
     sa.Column('seq', sa.Integer, primary_key=True, comment="시퀀스"),
     sa.Column('club', sa.Integer, nullable=False, comment="클럽id"),
     sa.Column('match', sa.Integer, nullable=False, comment="매치id"),
     sa.Column('position', ARRAY(sa.Integer), comment="포지션"),
     sa.Column('skill', sa.String(24), nullable=False, comment="레벨"),
     sa.Column('guest_number', sa.Integer, nullable=False, comment="모집인원"),
     sa.Column('match_fee', sa.Integer, comment="매치비용"),
     sa.Column('status', sa.String(24), nullable=False, comment="용병상태"),
     sa.Column('notice', sa.String(255), nullable=False, comment="공지사항")   
    )

def downgrade() -> None:
    op.drop_table('guest')
