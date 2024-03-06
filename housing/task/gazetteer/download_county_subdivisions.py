from prefect import get_run_logger, task

from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.gazetteer_ftp import GazetteerFTP
from housing.task.helper.file_syncer import FileSyncer


@task(name='Download Gazetteer county subdivision data', persist_result=True)
async def download_county_subdivisions(gazetteer_year: int, gazetteer_block_id: str, local_block_id: str):
    syncer = await FileSyncer.factory(
        (GazetteerFTP, gazetteer_block_id),
        (CensusLocalFileSystem, local_block_id),
        get_run_logger())

    get_run_logger().info(f'Downloading Gazetteer county subdivision definitions')
    return await syncer.sync(f'{gazetteer_year}_Gaz_cousubs_national.zip')
