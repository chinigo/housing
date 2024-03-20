from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import Base

if TYPE_CHECKING:
    import housing.model.reference.functional_status
    import housing.model.reference.state
    import housing.model.reference.subdivision
    import housing.model.tiger.county
    import housing.model.tiger.subdivision


class County(Base):
    __tablename__ = 'counties'
    __table_args__ = {'schema': 'ref'}

    fips: Mapped[str] = mapped_column(String(5), primary_key=True)
    state_fips: Mapped[str] = mapped_column(ForeignKey('ref.states.fips'))
    status_code: Mapped[str] = mapped_column(ForeignKey('ref.functional_statuses.code'))
    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=False)

    state: Mapped['housing.model.reference.state.State'] = relationship(
        back_populates='counties',
        foreign_keys=[state_fips]
    )
    subdivisions: Mapped['housing.model.reference.subdivision.Subdivision'] = relationship(
        back_populates='county'
    )
    status: Mapped['housing.model.reference.functional_status.FunctionalStatus'] = relationship(
        foreign_keys=[status_code]
    ) 

    tiger_county: Mapped['housing.model.tiger.county.County'] = relationship(
        back_populates='ref_county'
    )
    tiger_subdivisions: Mapped[List['housing.model.tiger.subdivision.Subdivision']] = relationship(
        back_populates='ref_county'
    )
