"""create auth_users table

Revision ID: ccad215e939a
Revises: 
Create Date: 2024-07-17 12:19:37.914169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccad215e939a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'auth_users',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('email', sa.String(50), unique = True, index = True),
        sa.Column('password', sa.String(50)),
        sa.Column('name', sa.String(50), index = True, nullable = True),
        sa.Column('address', sa.String(100), nullable = True),
        sa.Column('phone', sa.String(30), unique = True, nullable = True),
    )


def downgrade():
    op.drop_table('auth_users')
