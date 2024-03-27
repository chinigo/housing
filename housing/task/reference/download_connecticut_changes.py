
from prefect import task

from housing.block import CensusLocalFileSystem, ReferenceFTP, Registry
from housing.result.census_data_file import CensusDataFile
from housing.task.download_task import DownloadTask


@task(name='Download 2022 changes to Connecticut TIGER county definitions', persist_result=True)
async def download_connecticut_changes() -> CensusDataFile:
    return (await DownloadConnecticutChanges().sync())[0]


# See https://www.federalregister.gov/documents/2022/06/06/2022-12063/change-to-county-equivalents-in-the-state-of-connecticut
class DownloadConnecticutChanges(DownloadTask[ReferenceFTP, CensusLocalFileSystem]):
    @property
    def title(self) -> str:
        return 'Download changes to Connecticut TIGER county definitions'

    @property
    def path_segments(self) -> list[list[str]]:
        return [['ct_change', 'ct_cou_to_cousub_crosswalk.txt']]

    async def source_block(self) -> ReferenceFTP:
        return await Registry().reference_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry().reference_local()
