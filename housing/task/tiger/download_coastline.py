from prefect import get_run_logger, task

from housing.block import Registry
from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.tiger_ftp import TigerFTP
from housing.result import CensusDataFile
from housing.task.download_task import DownloadTask
from housing.task.helper import FileSyncer


@task(name='Download TIGER coastline', persist_result=True)
async def download_coastline(tiger_year: int) -> CensusDataFile:
    return (await DownloadCoastline(tiger_year).sync())[0]


class DownloadCoastline(DownloadTask[TigerFTP, CensusLocalFileSystem]):
    tiger_year: int

    def __init__(self, tiger_year: int):
        super().__init__()
        self.tiger_year = tiger_year

    @property
    def title(self) -> str: return f'TIGER coastline for {self.tiger_year}'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['COASTLINE', f'tl_{self.tiger_year}_us_coastline.zip']]

    async def source_block(self) -> TigerFTP:
        return await Registry().tiger_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().tiger_local()
