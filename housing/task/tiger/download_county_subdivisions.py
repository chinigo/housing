from prefect import get_run_logger, task

from housing.block import Registry
from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.tiger_ftp import TigerFTP
from housing.result import CensusDataFile
from housing.task.download_task import DownloadTask


@task(name='Download TIGER county subdivisions', persist_result=True)
async def download_county_subdivisions(tiger_year: int, state_fips_code: str) -> CensusDataFile:
    return (await DownloadCountySubdivisions(state_fips_code, tiger_year).sync())[0]


class DownloadCountySubdivisions(DownloadTask[TigerFTP, CensusLocalFileSystem]):
    tiger_year: int
    state_fips_code: str

    def __init__(self, state_fips_code: str, tiger_year: int):
        super().__init__()
        self.tiger_year = tiger_year
        self.state_fips_code = state_fips_code

    @property
    def title(self) -> str: return f'TIGER county subdivisions for state {
        self.state_fips_code} in {self.tiger_year}'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['COUSUB', f'tl_{self.tiger_year}_{self.state_fips_code}_cousub.zip']]

    async def source_block(self) -> TigerFTP:
        return await Registry().tiger_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().tiger_local()
