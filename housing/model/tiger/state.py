from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import PROJECT_SRID, Base

if TYPE_CHECKING:
    import housing.model.reference.state


class State(Base):
    __tablename__ = 'states'
    __table_args__ = {'schema': 'tiger'}

    fips: Mapped[str] = mapped_column(String(2), ForeignKey('ref.states.fips'), primary_key=True)

    geom: Column[Geometry] = Column(
        Geometry(geometry_type='MULTIPOLYGON', srid=PROJECT_SRID, spatial_index=True, nullable=False)
    )

    ref_state: Mapped['housing.model.reference.state.State'] = relationship(
        back_populates='tiger_state',
        foreign_keys=[fips],
    )
