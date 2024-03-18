from io import BytesIO
from typing import Any, Hashable

from geopandas.io import file
from pandas import DataFrame
from prefect import task

from housing.block import Registry
from housing.result.census_data_file import CensusDataFile
from housing.task.etl_task import ETLTask


@task(name='Upsert TIGER state boundaries', persist_result=True)
async def upsert_states(states_file: CensusDataFile, tiger_year: int) -> None:
    return await UpsertStates(states_file, tiger_year).run()


class UpsertStates(ETLTask[DataFrame, list[dict[Hashable, Any]], None]):
    states_file: CensusDataFile
    tiger_year: int

    def __init__(self, states_file: CensusDataFile, tiger_year: int):
        super().__init__()
        self.states_file = states_file
        self.tiger_year = tiger_year

    @property
    def title(self) -> str:
        return f'TIGER state boundaries for {self.tiger_year}'

    async def _extract(self) -> DataFrame:
        source = await Registry().tiger_local()
        source_content = await source.read_path(self.states_file.path)

        return file.read_file(BytesIO(source_content))

    async def _transform(self, extracted: DataFrame) -> Any:
        return extracted[
            ['GEOID', 'geometry']
        ].rename(
            columns={'GEOID': 'fips'}
        ).to_dict('records')

    async def _load(self, transformed: Any) -> None:
        return None
