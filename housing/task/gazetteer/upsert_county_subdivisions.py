from io import BytesIO
from typing import Any, Hashable
from zipfile import ZipFile

from numpy import array, array_split
from pandas import read_csv
from prefect import get_run_logger, task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.gazetteer import Subdivision
from housing.result import CensusDataFile
from housing.task.helper import session_from_block

INSERT_CHUNK_SIZE = 1_000


@task(name='Upsert Gazetteer county subdivisions data', persist_result=True)
async def upsert_county_subdivisions(subdivisions_file: CensusDataFile, gazetteer_year: int) -> None:
    logger = get_run_logger()
    source = await Registry().gazetteer_local()
    housing_db = await Registry().housing_database()

    source_content = await source.read_path(subdivisions_file.path)

    with ZipFile(BytesIO(source_content)) as zf:
        with zf.open(f'{gazetteer_year}_Gaz_cousubs_national.txt') as unzipped_content:
            df = read_csv(unzipped_content, delimiter='\t', dtype={'GEOID': str})

    records: list[dict[Hashable, Any]] = (df[
        ['FUNCSTAT', 'GEOID', 'NAME']
    ]).assign(**{
        'state_fips': df['GEOID'].str[0:2],
        'county_fips': df['GEOID'].str[0:5]
    }).rename(columns={
        'FUNCSTAT': 'status_code',
        'GEOID': 'fips',
        'NAME': 'name',
    }).to_dict('records')

    chunks = array_split(array(records), len(records) // INSERT_CHUNK_SIZE + 1)
    logger.info(f'Upserting {len(records)} county subdivision records in batches of {INSERT_CHUNK_SIZE}')

    async with session_from_block(housing_db) as sess:
        for idx, chunk in enumerate(chunks):
            logger.info(f'Upserting records {idx * INSERT_CHUNK_SIZE} through {(idx + 1) * INSERT_CHUNK_SIZE - 1}')
            await sess.execute(
                insert(Subdivision)
                .values(chunk.tolist())
                .on_conflict_do_update(
                    index_elements=[Subdivision.fips],
                    set_=dict(
                        county_fips=Subdivision.county_fips,
                        name=Subdivision.name,
                        state_fips=Subdivision.state_fips,
                        status_code=Subdivision.status_code,
                    )))
            await sess.commit()
