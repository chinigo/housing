
from asyncio import gather
from prefect import flow
from sqlalchemy import select

from housing import AreaSpecifier
from housing.block import Registry
from housing.model.reference import State
from housing.task.helper import session_from_block
from housing.task.tiger import download_counties, download_county_subdivisions, download_states, upsert_states, upsert_counties, upsert_county_subdivisions


async def resolve_state_fips_codes(area_specifier: AreaSpecifier) -> list[str]:
    async with session_from_block(await Registry().housing_database()) as session:
        return [state.fips for state in (await session.scalars(
            select(State)
            .where(State.postal_code.in_(area_specifier.keys()))
        ))]


@flow(name='Download TIGER source files', persist_result=True)
async def download_tiger(tiger_year: int, area_specifier: AreaSpecifier) -> None:
    state_fips_codes = await resolve_state_fips_codes(area_specifier)

    # coastlines = download_coastline.submit(tiger_year)
    states_file = download_states.submit(tiger_year, return_state=True)
    counties_file = download_counties.submit(tiger_year, return_state=True)
    county_subdivisions = [
        download_county_subdivisions.submit(tiger_year, state_fips_code) for state_fips_code in state_fips_codes
    ]
    states = upsert_states.submit(await states_file.result(), tiger_year, return_state=True)
    counties = upsert_counties.submit(await counties_file, tiger_year, return_state=True)

    await gather(counties, states, *county_subdivisions)
