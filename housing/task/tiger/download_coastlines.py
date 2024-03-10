from prefect import get_run_logger, task

from housing.block import Registry
from housing.task.helper import FileSyncer


@task(name='Download TIGER coastlines', persist_result=True)
async def download_coastlines(tiger_year: int, tiger_ftp_block_id: str, local_block_id: str):
    syncer = FileSyncer(await Registry().tiger_ftp, await Registry().tiger_local)

    get_run_logger().info(f'Downloading TIGER coastlines for {tiger_year}')
    return await syncer.sync('COASTLINE', f'tl_{tiger_year}_us_coastline.zip')
