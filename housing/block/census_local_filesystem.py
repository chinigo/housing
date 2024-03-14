from datetime import datetime
from functools import cached_property
from os import sep
from os.path import normpath
from typing import cast

from fsspec.implementations.local import LocalFileSystem
from pydantic import computed_field
from pydantic.v1 import Field

from housing.block.metadata_aware_filesystem import MetadataAwareFileSystem


class CensusLocalFileSystem(MetadataAwareFileSystem):
    basepath: str = Field(
        description="Directory in which to store local Census.gov files",
        example="./census_tiger_2023"
    )

    async def read_path(self, *path_segments: str) -> bytes:
        return cast(bytes, self._filesystem.read_bytes(self.fullpath(*path_segments)))

    async def write_path(self, content: bytes, *path_segments: str) -> None:
        p = self.fullpath(*path_segments)
        self._logger.debug(f'Writing {p}.')
        self._filesystem.write_bytes(p, content)
        self._logger.debug(f'Wrote {len(content)} bytes.')

    def size(self, *path_segments: str) -> int | None:
        try:
            return cast(int | None, self._filesystem.size(self.fullpath(*path_segments)))
        except FileNotFoundError:
            return None

    def mtime(self, *path_segments: str) -> datetime | None:
        try:
            return cast(datetime | None, self._filesystem.modified(self.fullpath(*path_segments)))
        except FileNotFoundError:
            return None

    @computed_field # type: ignore[misc]
    @cached_property
    def _base_path_segments(self) -> list[str]:
        return normpath(self.basepath).split(sep)

    @computed_field # type: ignore[misc]
    @cached_property
    def _filesystem(self) -> LocalFileSystem:
        return LocalFileSystem(auto_mkdir=True)
