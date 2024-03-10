from prefect import get_run_logger, task

from housing.block import Registry
from housing.task.helper import FileSyncer


@task(name='Download Gazetteer county data', persist_result=True)
async def download_counties(gazetteer_year: int):
    syncer = FileSyncer(await Registry().gazetteer_ftp, await Registry().gazetteer_local)

    get_run_logger().info(f'Downloading Gazetteer county definitions')
    return await syncer.sync(f'{gazetteer_year}_Gaz_counties_national.zip')
