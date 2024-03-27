from io import BytesIO
from typing import Any, Hashable

from pandas import DataFrame, read_csv
from prefect import task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.reference import County
from housing.result import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert TIGER county definitions', persist_result=True)
async def upsert_counties(counties_file: CensusDataFile) -> None:
    return await UpsertCounties(counties_file).run()


class UpsertCounties(ETLTask[DataFrame, list[dict[Hashable, Any]], None]):
    counties_file: CensusDataFile

    def __init__(self, counties_file: CensusDataFile):
        super().__init__()
        self.counties_file = counties_file

    @property
    def title(self) -> str:
        return 'TIGER county definitions'

    async def _extract(self) -> DataFrame:
        source = await Registry().reference_local()
        return read_csv(
            BytesIO(await source.read_path(self.counties_file.path)),
            delimiter='|',
            dtype={
                'COUNTYFP': str,
                'STATEFP': str
            }
        )

    async def _transform(self, extracted: DataFrame) -> list[dict[Hashable, Any]]:
        return extracted.assign(
            fips=lambda x: x['STATEFP'] + x['COUNTYFP']
        ).rename(columns={
            'COUNTYNAME': 'name',
            'FUNCSTAT': 'status_code',
            'STATEFP': 'state_fips',
        })[[
            'fips',
            'name',
            'state_fips',
            'status_code',
        ]].to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            await session.execute(
                insert(County)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[County.fips],
                    set_=dict(
                        name=County.name,
                        state_fips=County.state_fips,
                        status_code=County.status_code)))
            await session.commit()
