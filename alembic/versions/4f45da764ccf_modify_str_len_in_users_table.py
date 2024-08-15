"""modify str len in users table

Revision ID: 4f45da764ccf
Revises: ccad215e939a
Create Date: 2024-07-22 14:41:36.186992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f45da764ccf'
down_revision: Union[str, None] = 'ccad215e939a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('auth_users', 'password', type_ = sa.String(256))


def downgrade() -> None:
    pass
