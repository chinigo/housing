"""Create TIGER geo tables

Revision ID: b32be7d88032
Revises: 77b9891d7be5
Create Date: 2024-03-20 11:27:45.441211

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

from housing.model import PROJECT_SRID

# revision identifiers, used by Alembic.
revision: str = 'b32be7d88032'
down_revision: Union[str, None] = '77b9891d7be5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_geospatial_table(
        'states',
        sa.Column('fips', sa.String(length=2), nullable=False),
        sa.Column(
            'geom',
            Geometry(
                geometry_type='MULTIPOLYGON',
                srid=PROJECT_SRID,
                spatial_index=False,
                from_text='ST_GeomFromEWKT',
                name='geometry',
                nullable=False,
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['fips'], ['ref.states.fips']),
        sa.PrimaryKeyConstraint('fips'),
        schema='tiger',
    )
    op.create_geospatial_index(
        'idx_states_geom',
        'states',
        ['geom'],
        unique=False,
        schema='tiger',
        postgresql_using='gist',
        postgresql_ops={}
    )
    op.create_geospatial_table(
        'counties',
        sa.Column('fips', sa.String(length=5), nullable=False),
        sa.Column('state_fips', sa.String(length=2), nullable=False),
        sa.Column(
            'geom',
            Geometry(
                geometry_type='MULTIPOLYGON',
                srid=PROJECT_SRID,
                spatial_index=False,
                from_text='ST_GeomFromEWKT',
                name='geometry',
                nullable=False,
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['fips'], ['ref.counties.fips'], ),
        sa.ForeignKeyConstraint(['state_fips'], ['ref.states.fips'], ),
        sa.PrimaryKeyConstraint('fips'),
        schema='tiger'
    )
    op.create_geospatial_index(
        'idx_counties_geom',
        'counties',
        ['geom'],
        unique=False,
        schema='tiger',
        postgresql_using='gist',
        postgresql_ops={},
    )
    op.create_geospatial_table(
        'subdivisions',
        sa.Column('fips', sa.String(length=10), nullable=False),
        sa.Column('county_fips', sa.String(length=5), nullable=False),
        sa.Column('state_fips', sa.String(length=2), nullable=False),
        sa.Column(
            'geom',
            Geometry(
                geometry_type='MULTIPOLYGON',
                srid=PROJECT_SRID,
                spatial_index=False,
                from_text='ST_GeomFromEWKT',
                name='geometry',
                nullable=False,
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['county_fips'], ['ref.counties.fips'], ),
        sa.ForeignKeyConstraint(['fips'], ['ref.subdivisions.fips'], ),
        sa.ForeignKeyConstraint(['state_fips'], ['ref.states.fips'], ),
        sa.PrimaryKeyConstraint('fips'),
        schema='tiger'
    )
    op.create_geospatial_index(
        'idx_subdivisions_geom',
        'subdivisions',
        ['geom'],
        unique=False,
        schema='tiger',
        postgresql_using='gist',
        postgresql_ops={},
    )


def downgrade() -> None:
    op.drop_geospatial_index(
        'idx_subdivisions_geom',
        table_name='subdivisions',
        schema='tiger',
        postgresql_using='gist',
        column_name='geom',
    )
    op.drop_geospatial_table('subdivisions', schema='tiger')
    op.drop_geospatial_index(
        'idx_counties_geom',
        table_name='counties',
        schema='tiger',
        postgresql_using='gist',
        column_name='geom',
    )
    op.drop_geospatial_table('counties', schema='tiger')
    op.drop_geospatial_index(
        'idx_states_geom',
        table_name='states',
        schema='tiger',
        postgresql_using='gist',
        column_name='geom',
    )
    op.drop_geospatial_table('states', schema='tiger')
