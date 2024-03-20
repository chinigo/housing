from io import BytesIO
from typing import Any, Hashable

from pandas import DataFrame, read_csv
from prefect import task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.reference.state import State
from housing.result.census_data_file import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert TIGER state definitions', persist_result=True)
async def upsert_states(states_file: CensusDataFile) -> None:
    return await UpsertStates(states_file).run()


class UpsertStates(ETLTask[DataFrame, list[dict[Hashable, Any]], None]):
    states_file: CensusDataFile

    def __init__(self, states_file: CensusDataFile):
        super().__init__()
        self.states_file = states_file

    @property
    def title(self) -> str:
        return 'TIGER state definitions'

    async def _extract(self) -> DataFrame:
        source = await Registry().reference_local()
        return read_csv(
            BytesIO(await source.read_path(self.states_file.path)),
            delimiter='|',
            dtype={'STATEFP': str}
        )

    async def _transform(self, extracted: DataFrame) -> list[dict[Hashable, Any]]:
        return extracted[[
            'STATE',
            'STATEFP',
            'STATE_NAME'
        ]].rename(columns={
            'STATE': 'postal_code',
            'STATEFP': 'fips',
            'STATE_NAME': 'name',
        }).to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            await session.execute(
                insert(State)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[State.fips],
                    set_=dict(postal_code=State.postal_code, name=State.name)))
            await session.commit()
