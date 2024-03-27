"""Create TIGER reference tables

Revision ID: 77b9891d7be5
Revises: 1c5b7b72e12b
Create Date: 2024-03-20 11:25:32.601157

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = '77b9891d7be5'
down_revision: Union[str, None] = '1c5b7b72e12b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'functional_statuses',
        sa.Column('code', sa.String(length=2), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('associated_entity', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('code'),
        schema='ref'
    )
    op.create_table(
        'states',
        sa.Column('fips', sa.String(length=2), nullable=False),
        sa.Column('postal_code', sa.String(length=2), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('fips'),
        schema='ref'
    )
    op.create_index(op.f('ix_ref_states_name'), 'states', ['name'], unique=True, schema='ref')
    op.create_index(op.f('ix_ref_states_postal_code'), 'states', ['postal_code'], unique=True, schema='ref')
    op.create_table(
        'counties',
        sa.Column('fips', sa.String(length=5), nullable=False),
        sa.Column('state_fips', sa.String(length=2), nullable=False),
        sa.Column('status_code', sa.String(length=2), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['state_fips'], ['ref.states.fips'], ),
        sa.ForeignKeyConstraint(['status_code'], ['ref.functional_statuses.code'], ),
        sa.PrimaryKeyConstraint('fips'),
        schema='ref'
    )
    op.create_index(op.f('ix_ref_counties_name'), 'counties', ['name'], unique=False, schema='ref')
    op.create_table(
        'subdivisions',
        sa.Column('fips', sa.String(length=10), nullable=False),
        sa.Column('county_fips', sa.String(length=5), nullable=False),
        sa.Column('state_fips', sa.String(length=2), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status_code', sa.String(length=2), nullable=False),
        sa.ForeignKeyConstraint(['county_fips'], ['ref.counties.fips'], ),
        sa.ForeignKeyConstraint(['state_fips'], ['ref.states.fips'], ),
        sa.ForeignKeyConstraint(['status_code'], ['ref.functional_statuses.code'], ),
        sa.PrimaryKeyConstraint('fips'),
        schema='ref'
    )
    op.create_index(op.f('ix_ref_subdivisions_name'), 'subdivisions', ['name'], unique=False, schema='ref')


def downgrade() -> None:
    op.drop_index(op.f('ix_ref_subdivisions_name'), table_name='subdivisions', schema='ref')
    op.drop_table('subdivisions', schema='ref')
    op.drop_index(op.f('ix_ref_counties_name'), table_name='counties', schema='ref')
    op.drop_table('counties', schema='ref')
    op.drop_index(op.f('ix_ref_states_postal_code'), table_name='states', schema='ref')
    op.drop_index(op.f('ix_ref_states_name'), table_name='states', schema='ref')
    op.drop_table('states', schema='ref')
    op.drop_table('functional_statuses', schema='ref')
