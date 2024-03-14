from functools import cached_property

from pydantic import computed_field

from housing.block.census_ftp import CensusFTP


class ReferenceFTP(CensusFTP):
    @computed_field # type: ignore[misc]
    @cached_property
    def _base_path_segments(self) -> list[str]:
        return ['geo', 'docs', 'reference']
