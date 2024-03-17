from abc import abstractmethod, ABC
from logging import Logger, LoggerAdapter
from typing import Any, TypeVar, Generic

from prefect import get_run_logger

E = TypeVar('E')
T = TypeVar('T')
L = TypeVar('L')


class ETLTask(Generic[E, T, L], ABC):
    _logger: Logger | LoggerAdapter[Any]

    def __init__(self):
        self._logger = get_run_logger()

    async def run(self) -> L:
        self._logger.info(f'ETLing {self.title}')

        self._logger.debug(f'Extracting {self.title}')
        extracted = await self._extract()
        self._logger.debug(f'Done extracting {self.title}')

        self._logger.debug(f'Transforming {self.title}')
        transformed = await self._transform(extracted)
        self._logger.debug(f'Done transforming {self.title}')

        self._logger.debug(f'Loading {self.title}')
        loaded = await self._load(transformed)
        self._logger.debug(f'Done loading {self.title}')

        self._logger.info(f'Done ETLing {self.title}')
        return loaded

    @property
    @abstractmethod
    def title(self) -> str: pass

    @abstractmethod
    async def _extract(self) -> E: pass

    @abstractmethod
    async def _transform(self, extracted: E) -> T: pass

    @abstractmethod
    async def _load(self, transformed: T) -> L: pass
