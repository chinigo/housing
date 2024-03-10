from io import BytesIO

from pandas import read_csv
from prefect import get_run_logger, task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.gazetteer import State
from housing.task.helper import CensusDataFile, session_from_block


@task(name='Upsert Gazetteer state data', persist_result=True)
async def upsert_states(states_file: CensusDataFile):
    logger = get_run_logger()
    source = await Registry().reference_local
    housing_db = await Registry().housing_database

    source_content = await source.read_path(states_file.path)
    df = read_csv(BytesIO(source_content), delimiter='|', dtype={'STATEFP': str})

    records = df[['STATE', 'STATEFP', 'STATE_NAME']].rename(columns={
        'STATE': 'postal_code',
        'STATEFP': 'fips',
        'STATE_NAME': 'name',
    }).to_dict('records')

    logger.info(f'Upserting {len(records)} functional status definitions')

    async with session_from_block(housing_db) as sess:
        await sess.execute(
            insert(State)
            .values(records)
            .on_conflict_do_update(
                index_elements=[State.fips],
                set_=dict(postal_code=State.postal_code, name=State.name)))
        await sess.commit()
