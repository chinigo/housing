from prefect import get_run_logger, task

from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.tiger_ftp import TigerFTP
from housing.task.helper.file_syncer import FileSyncer


@task(name='Download TIGER coastlines', persist_result=True)
async def download_coastlines(tiger_year: int, tiger_ftp_block_id: str, local_block_id: str):
    logger = get_run_logger()
    syncer = await FileSyncer.factory(
        (TigerFTP, tiger_ftp_block_id),
        (CensusLocalFileSystem, local_block_id),
        logger)

    logger.info(f'Downloading TIGER coastlines for {tiger_year}')
    return await syncer.sync('COASTLINE', f'tl_{tiger_year}_us_coastline.zip')
