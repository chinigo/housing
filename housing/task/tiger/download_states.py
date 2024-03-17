from prefect import task

from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.registry import Registry
from housing.block.tiger_ftp import TigerFTP
from housing.result.census_data_file import CensusDataFile
from housing.task.download_task import DownloadTask


@task(name='Download TIGER states', persist_result=True)
async def download_states(tiger_year: int) -> CensusDataFile:
    return (await DownloadStates(tiger_year).sync())[0]


class DownloadStates(DownloadTask[TigerFTP, CensusLocalFileSystem]):
    tiger_year: int

    def __init__(self, tiger_year: int):
        super().__init__()
        self.tiger_year = tiger_year

    @property
    def title(
        self) -> str: return f'TIGER state boundaries for {self.tiger_year}'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['STATE', f'tl_{self.tiger_year}_us_state.zip']]

    async def source_block(self) -> TigerFTP:
        return await Registry().tiger_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().tiger_local()
