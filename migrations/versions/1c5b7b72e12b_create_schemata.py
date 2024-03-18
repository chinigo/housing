"""Create schemata

Revision ID: 1c5b7b72e12b
Revises: 
Create Date: 2024-03-06 15:57:18.039298

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.inspection import inspect


# revision identifiers, used by Alembic.
revision: str = '1c5b7b72e12b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA gz')
    op.execute('CREATE SCHEMA tiger')

def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS gz')
    op.execute('DROP SCHEMA IF EXISTS tiger')
