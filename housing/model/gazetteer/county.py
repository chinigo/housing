from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import Base

if TYPE_CHECKING:
    import housing.model.gazetteer.state
    import housing.model.gazetteer.subdivision
    import housing.model.tiger.county
    import housing.model.tiger.subdivision


class County(Base):
    __tablename__ = 'counties'
    __table_args__ = {'schema': 'gz'}

    fips: Mapped[str] = mapped_column(String(5), primary_key=True)
    state_fips: Mapped[str] = mapped_column(ForeignKey('gz.states.fips'))
    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=False)

    state: Mapped['housing.model.gazetteer.state.State'] = relationship(
        back_populates='counties',
        foreign_keys=[state_fips]
    )
    subdivisions: Mapped['housing.model.gazetteer.subdivision.Subdivision'] = relationship(
        back_populates='county'
    )

    tiger_county: Mapped['housing.model.tiger.county.County'] = relationship(
        back_populates='gazetteer_county'
    )
    tiger_subdivisions: Mapped[List['housing.model.tiger.subdivision.Subdivision']] = relationship(
        back_populates='gazetteer_county'
    )
