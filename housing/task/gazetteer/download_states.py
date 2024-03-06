from prefect import get_run_logger, task

from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.reference_ftp import ReferenceFTP
from housing.task.helper.file_syncer import FileSyncer


@task(name='Download Gazetteer state data', persist_result=True)
async def download_states(reference_ftp_block_id: str, reference_local_block_id: str):
    syncer = await FileSyncer.factory(
        (ReferenceFTP, reference_ftp_block_id),
        (CensusLocalFileSystem, reference_local_block_id),
        get_run_logger())

    get_run_logger().info(f'Downloading state definitions')
    return await syncer.sync('codes2020', 'national_state2020.txt')
