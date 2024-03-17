from asyncio import gather

from prefect import flow
from sqlalchemy import select

from housing.block import Registry
from housing.model.gazetteer import County, State
from housing.task.helper import session_from_block
from housing.task.tiger.download_coastline import download_coastline
from housing.task.tiger.download_counties import download_counties
from housing.task.tiger.download_county_subdivisions import \
    download_county_subdivisions
from housing.task.tiger.download_states import download_states


async def resolve_state_fips_codes(state_postal_codes: list[str]) -> list[str]:
    async with session_from_block(await Registry().housing_database()) as session:
        return [state.fips for state in (await session.scalars(
            select(State)
            .where(State.postal_code.in_(state_postal_codes))
        ))]


@flow(name='Download TIGER source files', persist_result=True)
async def download_tiger(tiger_year: int, state_postal_codes: list[str]) -> None:
    state_fips_codes = await resolve_state_fips_codes(state_postal_codes)

    coastlines = download_coastline.submit(tiger_year)
    counties = download_counties.submit(tiger_year)
    county_subdivisions = [
        download_county_subdivisions.submit(tiger_year, state_fips_code) for state_fips_code in state_fips_codes
    ]
    states = download_states.submit(tiger_year)

    await gather(coastlines, counties, *county_subdivisions, states)
