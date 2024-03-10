from prefect import get_run_logger, task

from housing.block import Registry
from housing.task.helper import FileSyncer


@task(name='Download Gazetteer state data', persist_result=True)
async def download_states():
    syncer = FileSyncer(await Registry().reference_ftp, await Registry().reference_local)

    get_run_logger().info(f'Downloading state definitions')
    return await syncer.sync('codes2020', 'national_state2020.txt')
