from housing.block import CensusLocalFileSystem, GazetteerFTP, Registry
from housing.task import DownloadTask


class DownloadCounties(DownloadTask[GazetteerFTP, CensusLocalFileSystem]):
    gazetteer_year: int

    def __init__(self, gazetteer_year: int):
        super().__init__()
        self.gazetteer_year = gazetteer_year

    @property
    def title(self) -> str:
        return 'Gazetteer county definitions'

    @property
    def path_segments(self) -> list[list[str]]:
        return [[f'{self.gazetteer_year}_Gaz_counties_national.zip']]

    async def source_block(self) -> GazetteerFTP:
        return await Registry().gazetteer_ftp()

    async def destination_block(self) -> CensusLocalFileSystem:
        return await Registry.gazetteer_local()
