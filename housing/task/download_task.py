from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

S = TypeVar('S')
# D = TypeVar('D', bound='DownloadTask')


class DownloadTask(Generic[S], ABC):
    @abstractmethod
    async def source_block(self) -> S:
        pass

    @abstractmethod
    async def destination_block(self) -> Any:
        pass

    @property
    @abstractmethod
    def path_segments(self) -> list[list[str]]:
        pass
