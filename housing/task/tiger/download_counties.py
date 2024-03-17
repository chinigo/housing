from prefect import get_run_logger, task

from housing.block import Registry
from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.tiger_ftp import TigerFTP
from housing.result import CensusDataFile
from housing.task.download_task import DownloadTask

@task(name='Download TIGER counties', persist_result=True)
async def download_counties(tiger_year: int) -> CensusDataFile:
    return (await DownloadCounties(tiger_year).sync())[0]


class DownloadCounties(DownloadTask[TigerFTP, CensusLocalFileSystem]):
    tiger_year: int

    def __init__(self, tiger_year: int):
        super().__init__()
        self.tiger_year = tiger_year

    @property
    def title(self) -> str: return f'TIGER counties for {self.tiger_year}'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['COUNTY', f'tl_{self.tiger_year}_us_county.zip']]

    async def source_block(self) -> TigerFTP:
        return await Registry().tiger_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().tiger_local()
