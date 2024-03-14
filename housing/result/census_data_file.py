import datetime
from os.path import join
from typing import Type, TypeVar

from pydantic.v1 import BaseModel, Field

from housing.block.metadata_aware_filesystem import MetadataAwareFileSystem

T = TypeVar('T', bound='CensusDataFile')


class CensusDataFile(BaseModel):
    path: str = Field(
        description='Path to the source file (relative to the dataset root directory)',
        example='/STATE/tl_2023_us_state.zip',
    )
    mtime: datetime.datetime | None = Field(
        description='Modification time of the file',
        example=datetime.datetime(2023, 1, 30),
    )
    size: int | None = Field(
        description='Bytesize of the file contents',
        example=1024,
    )

    @classmethod
    def from_block(cls: Type[T], block: MetadataAwareFileSystem, *path_segments: str) -> T:
        return cls(
            path=join(*path_segments),
            mtime=block.mtime(*path_segments),
            size=block.size(*path_segments))
