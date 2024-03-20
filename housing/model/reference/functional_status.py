from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Text

from housing.model import Base


class FunctionalStatus(Base):
    __tablename__ = 'functional_statuses'
    __table_args__ = {'schema': 'ref'}

    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    associated_entity: Mapped[str] = mapped_column(Text(), nullable=False)
