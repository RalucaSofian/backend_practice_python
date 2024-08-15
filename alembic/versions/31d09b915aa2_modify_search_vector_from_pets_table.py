"""modify search vector from pets table

Revision ID: 31d09b915aa2
Revises: aae442522d4d
Create Date: 2024-08-13 15:22:48.824582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy_searchable import sync_trigger


# revision identifiers, used by Alembic.
revision: str = '31d09b915aa2'
down_revision: Union[str, None] = 'aae442522d4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    sync_trigger(conn, 'pets', 'search_vector', ['name', 'species', 'description'])


def downgrade():
    conn = op.get_bind()
    sync_trigger(conn, 'pets', 'search_vector', ['name', 'species', 'description'])
