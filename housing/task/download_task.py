from abc import ABC, abstractmethod
from logging import Logger, LoggerAdapter
from prefect import get_run_logger
from housing.task.helper import FileSyncer
from os.path import join
from typing import Any, Generic, TypeVar

from housing.result import CensusDataFile
from housing.block.metadata_aware_filesystem import MetadataAwareFileSystem

S = TypeVar('S', bound='MetadataAwareFileSystem')
D = TypeVar('D', bound='MetadataAwareFileSystem')


class DownloadTask(Generic[S, D], ABC):
    _logger: Logger | LoggerAdapter[Any]

    def __init__(self):
        self._logger = get_run_logger()

    @property
    @abstractmethod
    def title(self) -> str: pass

    @property
    @abstractmethod
    def path_segments(self) -> list[list[str]]: pass

    @abstractmethod
    async def source_block(self) -> S: pass

    @abstractmethod
    async def destination_block(self) -> D: pass

    async def sync(self) -> list[CensusDataFile]:
        self._logger.info(f'Downloading {self.title}')
        syncer = FileSyncer(await self.source_block(), await self.destination_block())

        results = [await self._sync_one(syncer, segments) for segments in self.path_segments]

        self._logger.info(f'Done downloading {self.title}')

        return results

    async def _sync_one(self, syncer: FileSyncer, segments: list[str]) -> CensusDataFile:
        abs_path = join(*segments)
        self._logger.info(f'Downloading file {abs_path}')

        result = await syncer.sync(abs_path)
        self._logger.info(f'Done downloading file {abs_path}')

        return result
