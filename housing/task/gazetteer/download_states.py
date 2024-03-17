from prefect import task

from housing.block import CensusLocalFileSystem, ReferenceFTP, Registry
from housing.result.census_data_file import CensusDataFile
from housing.task.download_task import DownloadTask


@task(name='Download Gazetteer state data', persist_result=True)
async def download_states() -> CensusDataFile:
    return (await DownloadGazetteerStates().sync())[0]


class DownloadGazetteerStates(DownloadTask[ReferenceFTP, CensusLocalFileSystem]):
    @property
    def title(self) -> str:
        return 'Gazetteer state definitions'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['codes2020', 'national_state2020.txt']]

    async def source_block(self) -> ReferenceFTP:
        return await Registry().reference_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().reference_local()
