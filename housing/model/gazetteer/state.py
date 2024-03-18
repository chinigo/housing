from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import Base

if TYPE_CHECKING:
    import housing.model.gazetteer.county
    import housing.model.gazetteer.subdivision
    import housing.model.tiger.county
    import housing.model.tiger.state
    import housing.model.tiger.subdivision


class State(Base):
    __tablename__ = 'states'
    __table_args__ = {'schema': 'gz'}

    fips: Mapped[str] = mapped_column(String(2), primary_key=True)
    postal_code: Mapped[str] = mapped_column(String(2), index=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=True)

    counties: Mapped[List['housing.model.gazetteer.county.County']] = relationship(back_populates='state')
    subdivisions: Mapped[List['housing.model.gazetteer.subdivision.Subdivision']] = relationship(back_populates='state')

    tiger_state: Mapped['housing.model.tiger.state.State'] = relationship(back_populates='gazetteer_state')
    tiger_counties: Mapped[List['housing.model.tiger.county.County']] = relationship(back_populates='gazetteer_state')
    tiger_subdivisions: Mapped[List['housing.model.tiger.subdivision.Subdivision']] = relationship(back_populates='gazetteer_state')
