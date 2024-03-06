from logging import Logger
from typing import Type, TypeVar

from housing.block.metadata_aware_filesystem import MetadataAwareFileSystem
from housing.model.census_data_file import CensusDataFile

T = TypeVar('T', bound='FileSyncer')


class FileSyncer:
    def __init__(self, source_fs: MetadataAwareFileSystem, destination_fs: MetadataAwareFileSystem, logger: Logger):
        self.source_fs = source_fs
        self.destination_fs = destination_fs
        self._logger = logger

    @classmethod
    async def factory(
            cls: Type[T],
            source_block: tuple[Type[MetadataAwareFileSystem], str],
            destination_block: tuple[Type[MetadataAwareFileSystem], str],
            logger: Logger
    ) -> T:
        return FileSyncer(
            await source_block[0].load(source_block[1]),
            await destination_block[0].load(destination_block[1]),
            logger,
        )

    async def sync(self, *path_segments: str):
        source_file = CensusDataFile.from_block(self.source_fs, *path_segments)
        destination_file = CensusDataFile.from_block(self.destination_fs, *path_segments)

        if self._needs_update(source_file, destination_file, *path_segments):
            await self.destination_fs.write_path(await self.source_fs.read_path(*path_segments), *path_segments)

            destination_file.size = self.destination_fs.size(*path_segments)
            destination_file.mtime = self.destination_fs.mtime(*path_segments)

        return destination_file

    def _needs_update(self, source_file: CensusDataFile, destination_file: CensusDataFile, *path_segments: str):
        if destination_file.size is None or destination_file.mtime is None:
            self._logger.info(
                f'Destination file does not exist at {self.destination_fs.fullpath(*path_segments)}. Copying.')
            return True

        if destination_file.size != source_file.size:
            self._logger.info(
                f'Destination file size ({destination_file.size} bytes) does not match source file size ' +
                f'({source_file.size} bytes). Copying.')
            return True

        if destination_file.mtime < source_file.mtime:
            self._logger.info('Source file is more recent than destination file. Copying.')
            return True

        self._logger.info(
            f'Destination file {self.destination_fs.fullpath(*path_segments)} up to date. Skipping download.')
        return False
