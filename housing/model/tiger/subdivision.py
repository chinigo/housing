from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import PROJECT_SRID, Base

if TYPE_CHECKING:
    import housing.model.gazetteer.county
    import housing.model.gazetteer.state
    import housing.model.gazetteer.subdivision


class Subdivision(Base):
    __tablename__ = 'subdivisions'
    __table_args__ = {'schema': 'tiger'}

    fips: Mapped[str] = mapped_column(String(10), ForeignKey('gz.subdivisions.fips'), primary_key=True)
    county_fips: Mapped[str] = mapped_column(String(5), ForeignKey('gz.counties.fips'))
    state_fips: Mapped[str] = mapped_column(String(2), ForeignKey('gz.states.fips'))

    geom: Column[Geometry] = Column(
        Geometry(geometry_type='MULTIPOLYGON', srid=PROJECT_SRID, spatial_index=True, nullable=False)
    )

    gazetteer_subdivision: Mapped['housing.model.gazetteer.subdivision.Subdivision'] = relationship(
        back_populates='tiger_subdivision',
        foreign_keys=[fips],
    )
    gazetteer_county: Mapped['housing.model.gazetteer.county.County'] = relationship(
        back_populates='tiger_subdivisions',
        foreign_keys=[county_fips],
    )
    gazetteer_state: Mapped['housing.model.gazetteer.state.State'] = relationship(
        back_populates='tiger_subdivisions',
        foreign_keys=[state_fips],
    )
