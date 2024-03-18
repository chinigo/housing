from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import TYPE_CHECKING

from housing.model import SRID, Base

if TYPE_CHECKING:
  from housing.model.gazetteer import State as GazetteerState


class State(Base):
    __tablename__ = 'states'
    __table_args__ = {'schema': 'tiger'}

    fips: Mapped[str] = mapped_column(String(2), primary_key=True)
    gazetteer_state: Mapped['GazetteerState'] = relationship(
        back_populates='tiger_state')
    geom: Column[Geometry] = Column(
        Geometry(geometry_type='MULTIPOLYGON', srid=SRID, spatial_index=True, nullable=False)
    )
