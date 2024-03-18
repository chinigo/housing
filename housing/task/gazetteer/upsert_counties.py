from io import BytesIO
from typing import Any, Hashable
from zipfile import ZipFile

from pandas import DataFrame, read_csv
from prefect import task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.gazetteer import County
from housing.result import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert Gazetteer county data', persist_result=True)
async def upsert_counties(counties_file: CensusDataFile, gazetteer_year: int) -> None:
    return await UpsertCounties(counties_file, gazetteer_year).run()


class UpsertCounties(ETLTask[DataFrame, list[dict[Hashable, Any]], None]):
    counties_file: CensusDataFile
    gazetteer_year: int

    def __init__(self, counties_file: CensusDataFile, gazetteer_year: int):
        super().__init__()
        self.counties_file = counties_file
        self.gazetteer_year = gazetteer_year

    @property
    def title(self) -> str: return 'Census county definitions'

    async def _extract(self) -> DataFrame:
        source = await Registry().gazetteer_local()
        source_content = await source.read_path(self.counties_file.path)

        with ZipFile(BytesIO(source_content)) as zf:
            with zf.open(f'{self.gazetteer_year}_Gaz_counties_national.txt') as unzipped_content:
                return read_csv(unzipped_content, delimiter='\t', dtype={'GEOID': str})

    async def _transform(self, extracted: DataFrame) -> list[dict[Hashable, Any]]:
        return extracted[
            ['GEOID', 'NAME']
        ].assign(
            **{'state_fips': extracted['GEOID'].str[0:2]}
        ).rename(columns={
            'GEOID': 'fips',
            'NAME': 'name',
        }).to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            await session.execute(
                insert(County)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[County.fips],
                    set_=dict(
                        name=County.name,
                        state_fips=County.state_fips)))
            await session.commit()
