from io import BytesIO
from typing import Any, Hashable
from zipfile import ZipFile

from numpy import array, array_split
from pandas import DataFrame, read_csv
from prefect import get_run_logger, task
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model.reference import Subdivision
from housing.result import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block

INSERT_CHUNK_SIZE = 1_000


@task(name='Upsert TIGER county subdivision definitions', persist_result=True)
async def upsert_county_subdivisions(county_subdivisions_file: CensusDataFile) -> None:
    return await UpsertCountySubdivisions(county_subdivisions_file).run()


class UpsertCountySubdivisions(ETLTask[DataFrame, list[dict[Hashable, Any]], None]):
    county_subdivisions_file: CensusDataFile

    def __init__(self, county_subdivisions_file: CensusDataFile):
        super().__init__()
        self.county_subdivisions_file = county_subdivisions_file

    @property
    def title(self) -> str:
        return 'TIGER county subdivision definitions'

    async def _extract(self) -> DataFrame:
        source = await Registry().reference_local()

        return read_csv(
            BytesIO(await source.read_path(self.county_subdivisions_file.path)),
            delimiter='|',
            dtype={
                'COUNTYFP': str,
                'COUSUBFP': str,
                'STATEFP': str
            }
        )

    async def _transform(self, extracted: DataFrame) -> list[dict[Hashable, Any]]:
        return extracted.assign(
            county_fips=lambda x: x['STATEFP'] + x['COUNTYFP'],
            fips=lambda x: x['STATEFP'] + x['COUNTYFP'] + x['COUSUBFP'],
        ).rename(columns={
            'COUSUBNAME': 'name',
            'FUNCSTAT': 'status_code',
            'STATEFP': 'state_fips',
        })[[
            'county_fips',
            'fips',
            'name',
            'state_fips',
            'status_code',
        ]].to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        chunks = array_split(array(transformed), len(transformed) // INSERT_CHUNK_SIZE + 1)

        self._logger.debug(f'Upserting {len(transformed)} county subdivision records in batches of {INSERT_CHUNK_SIZE}')

        async with session_from_block(await Registry().housing_database()) as session:
            for idx, chunk in enumerate(chunks):
                self._logger.debug(f'Upserting records {
                                   idx * INSERT_CHUNK_SIZE} through {(idx + 1) * INSERT_CHUNK_SIZE - 1}')
                await session.execute(
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
                await session.commit()
