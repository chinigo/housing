from prefect import get_run_logger, task

from housing.block import CensusLocalFileSystem, GazetteerFTP, Registry
from housing.result import CensusDataFile
from housing.task import DownloadTask
from housing.task.helper import FileSyncer


class DownloadGazetteerCounties(DownloadTask[GazetteerFTP]):
    async def source_block(self) -> GazetteerFTP:
        return await Registry().gazetteer_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry.gazetteer_local()

    @property
    def path_segments(self) -> list[list[str]]:
        return []


@task(name='Download Gazetteer county data', persist_result=True)
async def download_counties(gazetteer_year: int) -> CensusDataFile:
    syncer = FileSyncer(await Registry().gazetteer_ftp(), await Registry().gazetteer_local())

    get_run_logger().info(f'Downloading Gazetteer county definitions')
    return await syncer.sync(f'{gazetteer_year}_Gaz_counties_national.zip')
