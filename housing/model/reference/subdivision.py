from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import Base

if TYPE_CHECKING:
    import housing.model.reference.county
    import housing.model.reference.functional_status
    import housing.model.reference.state
    import housing.model.tiger.subdivision


class Subdivision(Base):
    __tablename__ = 'subdivisions'
    __table_args__ = {'schema': 'ref'}

    fips: Mapped[str] = mapped_column(String(10), primary_key=True)
    county_fips: Mapped[str] = mapped_column(ForeignKey('ref.counties.fips'))
    state_fips: Mapped[str] = mapped_column(ForeignKey('ref.states.fips'))

    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=False)
    status_code: Mapped[str] = mapped_column(ForeignKey('ref.functional_statuses.code'))

    county: Mapped['housing.model.reference.county.County'] = relationship(
        back_populates='subdivisions',
        foreign_keys=[county_fips]
    )
    state: Mapped['housing.model.reference.state.State'] = relationship(
        back_populates='subdivisions',
        foreign_keys=[state_fips]
    )
    status: Mapped['housing.model.reference.functional_status.FunctionalStatus'] = relationship(
        foreign_keys=[status_code]
    )
    tiger_subdivision: Mapped['housing.model.tiger.subdivision.Subdivision'] = relationship(
        back_populates='ref_subdivision'
    )