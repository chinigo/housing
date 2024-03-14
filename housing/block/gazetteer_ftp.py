from functools import cached_property

from pydantic import computed_field
from pydantic.v1 import Field

from housing.block.census_ftp import CensusFTP


class GazetteerFTP(CensusFTP):
    gazetteer_year: int = Field(
        description='Year of Gazetteer dataset in which we are interested',
        example=2023,
    )

    @computed_field # type: ignore[misc]
    @cached_property
    def _base_path_segments(self) -> list[str]:
        return ['geo', 'docs', 'maps-data', 'data', 'gazetteer', f'{self.gazetteer_year}_Gazetteer']
