"""add content column to posts table

Revision ID: ed58dbf3e63d
Revises: 28799384715a
Create Date: 2023-08-14 19:22:07.364001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed58dbf3e63d'
down_revision: Union[str, None] = '28799384715a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
