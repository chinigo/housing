from io import BytesIO
from typing import Any, Hashable, cast
from shapely import wkt

from geopandas import read_file, GeoDataFrame
from pandas import DataFrame
from prefect import task
from sqlalchemy import CursorResult
from sqlalchemy.dialects.postgresql import insert

from housing.block import Registry
from housing.model import PROJECT_CRS
from housing.model.tiger import State as TigerState
from housing.result.census_data_file import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert TIGER state boundaries', persist_result=False)
async def upsert_states(states_file: CensusDataFile, tiger_year: int) -> None:
    return await UpsertStates(states_file, tiger_year).run()


class UpsertStates(ETLTask[GeoDataFrame, list[dict[Hashable, Any]], None]):
    states_file: CensusDataFile
    tiger_year: int

    def __init__(self, states_file: CensusDataFile, tiger_year: int):
        super().__init__()
        self.states_file = states_file
        self.tiger_year = tiger_year

    @property
    def title(self) -> str:
        return f'TIGER state boundaries for {self.tiger_year}'

    async def _extract(self) -> GeoDataFrame:
        source = await Registry().tiger_local()
        source_content = await source.read_path(self.states_file.path)

        extracted = read_file(BytesIO(source_content))
        if isinstance(extracted, GeoDataFrame):
            return extracted

        raise ValueError(f'Expected a GeoDataFrame, got a {extracted.__class__}')

    async def _transform(self, extracted: GeoDataFrame) -> list[dict[Hashable, Any]]:
        return cast(DataFrame, extracted.to_crs(PROJECT_CRS))[
            ['GEOID', 'geometry']
        ].assign(
            geom=lambda x: x.geometry.map(wkt.dumps)
        ).rename(
            columns={'GEOID': 'fips'}
        )[
            ['fips', 'geom']
        ].to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            result = await session.execute(
                insert(TigerState)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[TigerState.fips],
                    set_=dict(geom=TigerState.geom)
                )
            )

            await session.commit()
