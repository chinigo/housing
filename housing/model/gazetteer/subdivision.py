from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import Base

if TYPE_CHECKING:
    from housing.model.gazetteer import County, FunctionalStatus, State


class Subdivision(Base):
    __tablename__ = 'subdivisions'
    __table_args__ = {'schema': 'gz'}

    fips: Mapped[str] = mapped_column(String(10), primary_key=True)
    county_fips: Mapped[str] = mapped_column(ForeignKey('gz.counties.fips'))
    state_fips: Mapped[str] = mapped_column(ForeignKey('gz.states.fips'))

    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=False)
    status_code: Mapped[str] = mapped_column(ForeignKey('gz.functional_statuses.code'))

    # county: Mapped['County'] = relationship(back_populates='subdivisions', foreign_keys=[county_fips])
    # state: Mapped['State'] = relationship(back_populates='subdivisions', foreign_keys=[state_fips])
    # status: Mapped['FunctionalStatus'] = relationship(foreign_keys=[status_code])
