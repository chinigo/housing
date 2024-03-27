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
from housing.model.tiger import Subdivision
from housing.result.census_data_file import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Upsert TIGER county subdivision boundaries', persist_result=True)
async def upsert_county_subdivisions(county_subdivisions_file: CensusDataFile, tiger_year: int) -> None:
    return await UpsertCountySubdivisions(county_subdivisions_file, tiger_year).run()


class UpsertCountySubdivisions(ETLTask[GeoDataFrame, list[dict[Hashable, Any]], None]):
    county_subdivisions_file: CensusDataFile
    tiger_year: int

    def __init__(self, county_subdivisions_file: CensusDataFile, tiger_year: int):
        super().__init__()
        self.county_subdivisions_file = county_subdivisions_file
        self.tiger_year = tiger_year

    @property
    def title(self) -> str:
        return f'TIGER county subdivision boundaries for {self.tiger_year}'

    async def _extract(self) -> GeoDataFrame:
        source = await Registry().tiger_local()
        source_content = await source.read_path(self.county_subdivisions_file.path)

        extracted = read_file(BytesIO(source_content))
        if isinstance(extracted, GeoDataFrame):
            return extracted

        raise ValueError(f'Expected a GeoDataFrame, got a {extracted.__class__}')

    async def _transform(self, extracted: GeoDataFrame) -> list[dict[Hashable, Any]]:
        return cast(
            DataFrame, extracted.to_crs(PROJECT_CRS)
        ).rename(
            columns={'GEOID': 'fips'}
        ).assign(
            geom=lambda x: x.geometry.map(wkt.dumps),
            state_fips=lambda x: x.fips.str[0:2],
            county_fips=lambda x: x.fips.str[0:5]
        )[
            [
                'county_fips',
                'fips',
                'geom',
                'state_fips',
            ]
        ].to_dict('records')

    async def _load(self, transformed: list[dict[Hashable, Any]]) -> None:
        async with session_from_block(await Registry().housing_database()) as session:
            await session.execute(
                insert(Subdivision)
                .values(transformed)
                .on_conflict_do_update(
                    index_elements=[Subdivision.fips],
                    set_=dict(
                        geom=Subdivision.geom,
                        county_fips=Subdivision.county_fips,
                        state_fips=Subdivision.state_fips
                    )
                )
            )

            await session.commit()
