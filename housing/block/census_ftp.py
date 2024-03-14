import re
from abc import ABC
from datetime import datetime
from functools import cached_property
from typing import Any, cast

from fsspec.implementations.ftp import FTPFileSystem
from pydantic import computed_field
from pydantic.v1 import Field

from housing.block.metadata_aware_filesystem import MetadataAwareFileSystem


class CensusFTP(MetadataAwareFileSystem, ABC):
    host_name: str = Field(
        default='ftp2.census.gov',
        description='TIGER FTP server hostname',
        example='ftp2.census.gov',
    )

    async def read_path(self, *path_segments: str) -> bytes:
        p = self.fullpath(*path_segments)
        self._logger.debug(f'Downloading file {p} from {self.host_name}.')
        contents = self._filesystem.read_bytes(p)

        self._logger.debug(f'Downloaded {len(contents)} bytes.')

        return cast(bytes, contents)

    async def write_path(self, content: bytes, *path_segments: str) -> None:
        raise NotImplementedError('Cannot write to Census.gov FTP server')

    def mtime(self, *path_segments: str) -> datetime | None:
        # Times are assumed to be GMT as per spec
        # See https://www.rfc-editor.org/rfc/rfc3659.html#section-3
        response = self._run_command(f'MDTM {self.fullpath(*path_segments)}')
        if response is None:
            return None

        return datetime.strptime(f'{response}-+0000', '%Y%m%d%H%M%S-%z')

    def size(self, *path_segments: str) -> int | None:
        # See https://www.rfc-editor.org/rfc/rfc3659.html#section-4
        response = self._run_command(f'SIZE {self.fullpath(*path_segments)}')
        if response is None:
            return None

        return int(response)

    @computed_field # type: ignore[misc]
    @cached_property
    def _filesystem(self) -> FTPFileSystem:
        return FTPFileSystem(host=self.host_name)

    def _run_command(self, cmd: str) -> str | None | Any:
        self._logger.debug(f'Running command on {self.host_name}: {cmd}')
        try:
            resp = self._filesystem.ftp.sendcmd(cmd)
            self._logger.debug(f'Got response: {resp}')
            return re.findall(r'\d+\s(.*)', resp)[0]
        except ValueError as e:
            self._logger.error(f'Got error: {e}')
            return None
