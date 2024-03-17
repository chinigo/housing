from prefect import task
from housing.result.census_data_file import CensusDataFile
from housing.task.gazetteer.download_counties import DownloadCounties
from housing.task.gazetteer.download_county_subdivisions import DownloadGazetteerCountySubdivisions
from housing.task.gazetteer.download_states import DownloadGazetteerStates
from housing.task.gazetteer.upsert_counties import upsert_counties
from housing.task.gazetteer.upsert_county_subdivisions import upsert_county_subdivisions
from housing.task.gazetteer.upsert_functional_statuses import upsert_functional_statuses
from housing.task.gazetteer.upsert_states import upsert_states


@task(name='Download Gazetteer county data', persist_result=True)
async def download_counties(gazetteer_year: int) -> CensusDataFile:
    return (await DownloadCounties(gazetteer_year).sync())[0]


@task(name='Download Gazetteer county subdivision data', persist_result=True)
async def download_county_subdivisions(gazetteer_year: int) -> CensusDataFile:
    return (await DownloadGazetteerCountySubdivisions(gazetteer_year).sync())[0]


@task(name='Download Gazetteer state data', persist_result=True)
async def download_states() -> CensusDataFile:
    return (await DownloadGazetteerStates().sync())[0]

__all__ = [
    'download_counties',
    'download_county_subdivisions',
    'download_states',
    'upsert_counties',
    'upsert_functional_statuses',
    'upsert_states',
    'upsert_county_subdivisions'
]
