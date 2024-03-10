from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from housing.model import Base

if TYPE_CHECKING:
    from housing.model.gazetteer import County, Subdivision


class State(Base):
    __tablename__ = 'states'
    __table_args__ = {'schema': 'gz'}

    fips: Mapped[str] = mapped_column(String(2), primary_key=True)
    postal_code: Mapped[str] = mapped_column(String(2), index=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=True)

    counties: Mapped[List['County']] = relationship(back_populates='state')
    subdivisions: Mapped[List['Subdivision']] = relationship(back_populates='state')
