from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
from logging import Logger, LoggerAdapter
from os import sep
from os.path import join
from typing import Any

from prefect.blocks.core import Block
from prefect.logging.loggers import get_run_logger
from pydantic import computed_field


class MetadataAwareFileSystem(Block, ABC):
    @computed_field # type: ignore[misc]
    @cached_property
    def _logger(self) -> Logger | LoggerAdapter[Any]:
        return get_run_logger()

    def fullpath(self, *path_segments: str) -> str:
        return join(sep, *self._base_path_segments, *path_segments)

    @abstractmethod
    async def read_path(self, *path_segments: str) -> bytes:
        pass

    @abstractmethod
    async def write_path(self, content: bytes, *path_segments: str) -> None:
        pass

    @abstractmethod
    def mtime(self, *path_segments: str) -> datetime | None:
        pass

    @abstractmethod
    def size(self, *path_segments: str) -> int | None:
        pass

    @cached_property
    @abstractmethod
    def _base_path_segments(self) -> list[str]:
        pass
