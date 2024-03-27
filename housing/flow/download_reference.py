from prefect import flow

from housing.task.reference import *


@flow(name='Download TIGER reference files', persist_result=True)
async def download_reference() -> None:
    functional_statuses = upsert_functional_statuses.submit(return_state=True)

    downloaded_states = download_states.submit(return_state=True)
    downloaded_counties = download_counties.submit(return_state=True)
    downloaded_connecticut_changes = download_connecticut_changes.submit(return_state=True)
    downloaded_county_subdivisions = download_county_subdivisions.submit(return_state=True)

    upserted_states = upsert_states.submit(await downloaded_states, return_state=True)
    upserted_counties = upsert_counties.submit(
        await downloaded_counties,
        wait_for=[await upserted_states],
        return_state=True,
    )
    upserted_subdivisions = upsert_county_subdivisions.submit(
        await downloaded_county_subdivisions,
        wait_for=[await functional_statuses, await upserted_counties],
        return_state=True,
    )
    await fix_connecticut.submit(
        await downloaded_connecticut_changes,
        wait_for=[await upserted_subdivisions],
        return_state=True,
    )
