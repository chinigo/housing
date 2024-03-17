from housing.block import CensusLocalFileSystem, ReferenceFTP, Registry
from housing.task.download_task import DownloadTask


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
