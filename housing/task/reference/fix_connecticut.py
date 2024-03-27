from io import StringIO
from logging import getLogger, DEBUG
from re import compile
from typing import Any, Hashable, cast

from pandas import DataFrame, read_csv
from prefect import task
from sqlalchemy import delete, select

from housing.block import Registry
from housing.model.reference import County, Subdivision
from housing.result import CensusDataFile
from housing.task.etl_task import ETLTask
from housing.task.helper import session_from_block


@task(name='Fix Connecticut TIGER county definitions', persist_result=True)
async def fix_connecticut(connecticut_changes_file: CensusDataFile) -> None:
    await FixConnecticut(connecticut_changes_file).run()


class FixConnecticut(ETLTask[DataFrame, tuple[list[County], list[Subdivision]], None]):
    connecticut_changes_file: CensusDataFile

    def __init__(self, connecticut_changes_file: CensusDataFile):
        super().__init__()
        self.connecticut_changes_file = connecticut_changes_file

    @property
    def title(self) -> str:
        return 'Fix Connecticut TIGER county definitions'

    async def _extract(self) -> DataFrame:
        source = await Registry().reference_local()

        raw = StringIO((await source.read_path(self.connecticut_changes_file.path)).decode())
        filtered = StringIO()

        # There's junk at the end of the source file. Only copy up to the first empty line.
        for line in raw.readlines():
            if line == '\n':
                break
            filtered.write(line)

        filtered.seek(0)
        return read_csv(filtered, delimiter='|', dtype={
            'STATEFP\n(INCITS38)': str,
            'NEW_COUNTYFP\n(INCITS31)': str,
            'OLD_COUSUB_GEOID': str,
            'COUSUBFP': str,
        })

    async def _transform(self, extracted: DataFrame) -> tuple[list[County], list[Subdivision]]:
        data = extracted.rename(columns={
            'COUSUBFP': 'county_subdivision_fips',
            'COUSUB_FUNCSTAT': 'new_county_subdivision_status_code',
            'OLD_COUSUB_GEOID': 'old_county_subdivision_fips',
            'COUSUB_NAMELSAD': 'new_county_subdivision_name',
            'NEW_COUNTYFP\n(INCITS31)': 'county_fips',
            'NEW_COUNTY_NAMELSAD': 'new_county_name',
            'STATEFP\n(INCITS38)': 'state_fips',
        }).assign(
            new_county_fips=lambda x: x['state_fips'] + x['county_fips'],
            new_county_subdivision_fips=lambda x: x['state_fips'] + x['county_fips'] + x['county_subdivision_fips'],
        )[[
            'new_county_fips',
            'new_county_name',
            'new_county_subdivision_fips',
            'new_county_subdivision_name',
            'new_county_subdivision_status_code',
            'old_county_subdivision_fips',
            'state_fips',
        ]]

        return (self.new_counties(data), self.new_subdivisions(data))

    async def _load(self, transformed: tuple[list[County], list[Subdivision]]) -> None:
        new_counties = transformed[0]
        new_subdivisions = transformed[1]

        async with session_from_block(await Registry().housing_database()) as session:
            for county in (await session.execute(
                select(County)
                .where(County.state_fips == '09')
                .where(County.fips.not_in([c.fips for c in new_counties]))
            )).scalars():
                await session.delete(county)

            for county in new_counties:
                await session.merge(county)

            for subdivision in (await session.execute(
                select(Subdivision)
                .where(Subdivision.state_fips == '09')
                .where(Subdivision.fips.not_in([s.fips for s in new_subdivisions]))
            )).scalars():
                await session.delete(subdivision)
            
            for subdivision in new_subdivisions:
                await session.merge(subdivision)

            await session.commit()

            return None

    def new_counties(self, extracted: DataFrame) -> list[County]:
        return [
            County(
                fips=c[0],
                state_fips=c[1],
                name=c[2],
                status_code='A'
            )
            for c in cast(list[tuple], list(
                extracted.groupby(['new_county_fips', 'state_fips', 'new_county_name']).indices
            ))
        ]

    def new_subdivisions(self, extracted: DataFrame) -> list[Subdivision]:
        return [
            Subdivision(
                fips=s['new_county_subdivision_fips'],
                county_fips=s['new_county_fips'],
                state_fips=s['state_fips'],
                name=s['new_county_subdivision_name'],
                status_code=s['new_county_subdivision_status_code']
            )
            for s in extracted.to_dict('records')
        ]
