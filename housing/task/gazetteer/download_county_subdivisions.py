from prefect import get_run_logger, task

from housing.block import Registry
from housing.result import CensusDataFile
from housing.task.helper import FileSyncer


@task(name='Download Gazetteer county subdivision data', persist_result=True)
async def download_county_subdivisions(gazetteer_year: int) -> CensusDataFile:
    syncer = FileSyncer(await Registry().gazetteer_ftp(), await Registry().gazetteer_local())

    get_run_logger().info(f'Downloading Gazetteer county subdivision definitions')
    return await syncer.sync(f'{gazetteer_year}_Gaz_cousubs_national.zip')
