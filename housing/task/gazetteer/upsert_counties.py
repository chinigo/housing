from io import BytesIO
from zipfile import ZipFile

from pandas import read_csv
from prefect import get_run_logger, task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.gazetteer import County
from housing.task.helper import CensusDataFile, session_from_block


@task(name='Upsert Gazetteer county data', persist_result=True)
async def upsert_counties(counties_file: CensusDataFile, gazetteer_year: int):
    logger = get_run_logger()
    source = await Registry().gazetteer_local
    housing_db = await Registry().housing_database

    source_content = await source.read_path(counties_file.path)

    with ZipFile(BytesIO(source_content)) as zf:
        with zf.open(f'{gazetteer_year}_Gaz_counties_national.txt') as unzipped_content:
            df = read_csv(unzipped_content, delimiter='\t', dtype={'GEOID': str})

    records = ((df[
        ['GEOID', 'NAME']
    ]).assign(
        **{'state_fips': df['GEOID'].str[0:2]}
    ).rename(columns={
        'GEOID': 'fips',
        'NAME': 'name',
    })).to_dict('records')

    logger.info(f'Upserting {len(records)} county records')

    async with session_from_block(housing_db) as sess:
        await sess.execute(
            insert(County)
            .values(records)
            .on_conflict_do_update(
                index_elements=[County.fips],
                set_=dict(
                    name=County.name,
                    state_fips=County.state_fips)))
        await sess.commit()
