from io import BytesIO

from pandas import read_csv
from prefect import get_run_logger, task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.gazetteer import FunctionalStatus
from housing.task.helper import session_from_block


@task(name='Upsert Gazetteer functional status definitions', persist_result=True)
async def upsert_functional_statuses() -> None:
    logger = get_run_logger()
    local_data = await Registry().local_data()
    housing_db = await Registry().housing_database()

    source_content = await local_data.read_path('census.gov', 'geo', 'pdfs', 'reference', 'functional_status_codes.csv')

    records = read_csv(BytesIO(source_content)).to_dict('records')

    logger.info(f'Upserting {len(records)} functional status definitions')

    async with session_from_block(housing_db) as sess:
        await sess.execute(
            insert(FunctionalStatus)
            .values(records)
            .on_conflict_do_update(
                index_elements=[FunctionalStatus.code],
                set_=dict(
                    description=FunctionalStatus.description,
                    associated_entity=FunctionalStatus.associated_entity)))
        await sess.commit()
