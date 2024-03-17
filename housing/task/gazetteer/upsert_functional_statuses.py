from io import BytesIO
from typing import Any, Hashable

from pandas import DataFrame, read_csv
from prefect import task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.gazetteer import FunctionalStatus
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert Gazetteer functional status definitions', persist_result=True)
async def upsert_functional_statuses() -> None:
    return await UpsertFunctionalStatuses().run()


class UpsertFunctionalStatuses(ETLTask[DataFrame, list[dict[Hashable, Any]], None]):
    @property
    def title(self) -> str: return 'Functional status definitions'

    async def _extract(self) -> DataFrame:
        local_data = await Registry().local_data()
        return read_csv(BytesIO(await local_data.read_path('census.gov', 'geo', 'pdfs', 'reference', 'functional_status_codes.csv')))

    async def _transform(self, extracted: DataFrame) -> list[dict[Hashable, Any]]:
        return extracted.to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            await session.execute(
                insert(FunctionalStatus)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[FunctionalStatus.code],
                    set_=dict(
                        description=FunctionalStatus.description,
                        associated_entity=FunctionalStatus.associated_entity)))
            await session.commit()
