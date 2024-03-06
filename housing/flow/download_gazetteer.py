from prefect import flow

from housing.task.gazetteer.download_counties import download_counties
from housing.task.gazetteer.download_county_subdivisions import download_county_subdivisions
from housing.task.gazetteer.download_states import download_states


@flow(name='Download Gazetteer source files', persist_result=True)
def download_gazetteer(gazetteer_year: int = 2023):
    gazetteer_ftp_block_id = f'gazetteer-ftp-{gazetteer_year}'
    gazetteer_local_block_id = f'gazetteer-local-{gazetteer_year}'
    reference_ftp_block_id = f'reference-ftp'
    reference_local_block_id = f'reference-local'

    download_states(reference_ftp_block_id, reference_local_block_id)
    download_counties(gazetteer_year, gazetteer_ftp_block_id, gazetteer_local_block_id)
    download_county_subdivisions(gazetteer_year, gazetteer_ftp_block_id, gazetteer_local_block_id)
