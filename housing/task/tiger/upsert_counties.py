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
from housing.model.tiger import County
from housing.result.census_data_file import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert TIGER county boundaries', persist_result=True)
async def upsert_counties(counties_file: CensusDataFile, tiger_year: int) -> None:
    return await UpsertCounties(counties_file, tiger_year).run()


class UpsertCounties(ETLTask[GeoDataFrame, list[dict[Hashable, Any]], None]):
    counties_file: CensusDataFile
    tiger_year: int

    def __init__(self, counties_file: CensusDataFile, tiger_year: int):
        super().__init__()
        self.counties_file = counties_file
        self.tiger_year = tiger_year

    @property
    def title(self) -> str:
        return f'TIGER county boundaries for {self.tiger_year}'

    async def _extract(self) -> GeoDataFrame:
        source = await Registry().tiger_local()
        source_content = await source.read_path(self.counties_file.path)

        extracted = read_file(BytesIO(source_content))
        if isinstance(extracted, GeoDataFrame):
            return extracted

        raise ValueError(f'Expected a GeoDataFrame, got a {extracted.__class__}')

    async def _transform(self, extracted: GeoDataFrame) -> list[dict[Hashable, Any]]:
        return cast(DataFrame, extracted.to_crs(PROJECT_CRS))[
            ['GEOID', 'geometry']
        ].rename(
            columns={'GEOID': 'fips'}
        ).assign(
            geom=lambda x: x.geometry.map(wkt.dumps),
            state_fips=lambda x: x.fips.str[0:2],
        )[
            ['fips', 'state_fips', 'geom']
        ].to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            await session.execute(
                insert(County)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[County.fips],
                    set_=dict(geom=County.geom, state_fips=County.state_fips)
                )
            )

            await session.commit()
