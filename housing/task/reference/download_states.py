from prefect import task

from housing.block import CensusLocalFileSystem, ReferenceFTP, Registry
from housing.result.census_data_file import CensusDataFile
from housing.task.download_task import DownloadTask


@task(name='Download TIGER state definitions', persist_result=True)
async def download_states() -> CensusDataFile:
    return (await DownloadStates().sync())[0]


class DownloadStates(DownloadTask[ReferenceFTP, CensusLocalFileSystem]):
    @property
    def title(self) -> str:
        return 'TIGER state definitions'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['codes2020', 'national_state2020.txt']]

    async def source_block(self) -> ReferenceFTP:
        return await Registry().reference_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().reference_local()
