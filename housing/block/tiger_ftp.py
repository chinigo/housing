from functools import cached_property

from pydantic import computed_field
from pydantic.v1 import Field

from housing.block.census_ftp import CensusFTP


class TigerFTP(CensusFTP):
    tiger_year: int = Field(
        description='Year of TIGER dataset in which we are interested',
        example=2023,
    )

    @computed_field # type: ignore[misc]
    @cached_property
    def _base_path_segments(self) -> list[str]:
        return ['geo', 'tiger', f'TIGER{self.tiger_year}']
