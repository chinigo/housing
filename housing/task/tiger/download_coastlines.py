from prefect import get_run_logger, task

from housing.block import Registry
from housing.task.helper import FileSyncer
from housing.result import CensusDataFile


@task(name='Download TIGER coastlines', persist_result=True)
async def download_coastlines(tiger_year: int) -> CensusDataFile:
    syncer = FileSyncer(await Registry().tiger_ftp(), await Registry().tiger_local())

    get_run_logger().info(f'Downloading TIGER coastlines for {tiger_year}')
    return await syncer.sync('COASTLINE', f'tl_{tiger_year}_us_coastline.zip')
