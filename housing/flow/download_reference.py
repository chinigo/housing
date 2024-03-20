from prefect import flow

from housing.task.reference import *


@flow(name='Download TIGER reference files', persist_result=True)
async def download_reference() -> None:
    functional_statuses = upsert_functional_statuses.submit()

    downloaded_states = download_states.submit()
    downloaded_counties = download_counties.submit()
    downloaded_county_subdivisions = download_county_subdivisions.submit()

    upserted_states = upsert_states.submit(await downloaded_states)
    upserted_counties = upsert_counties.submit(
        await downloaded_counties,
        wait_for=[await upserted_states]
    )

    await upsert_county_subdivisions.submit(
        await downloaded_county_subdivisions,
        wait_for=[await upserted_counties, await functional_statuses]
    )
