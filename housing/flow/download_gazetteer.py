from prefect import flow

from housing.task.gazetteer import *


@flow(name='Download Gazetteer source files', persist_result=True)
async def download_gazetteer(gazetteer_year: int) -> None:
    functional_statuses = upsert_functional_statuses.submit()

    downloaded_states = download_states.submit()
    downloaded_counties = download_counties.submit(gazetteer_year)
    downloaded_county_subdivisions = download_county_subdivisions.submit(
        gazetteer_year)

    upserted_states = upsert_states.submit(await downloaded_states)
    upserted_counties = upsert_counties.submit(
        await downloaded_counties, gazetteer_year,
        wait_for=[await upserted_states]
    )

    await upsert_county_subdivisions.submit(
        await downloaded_county_subdivisions, gazetteer_year,
        wait_for=[await upserted_counties, await functional_statuses]
    )
