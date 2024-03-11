from prefect import flow

from housing.task.gazetteer import *


@flow(name='Download Gazetteer source files', persist_result=True)
async def download_gazetteer(gazetteer_year: int):
    await upsert_functional_statuses()
    await upsert_states(await download_states())
    await upsert_counties(await download_counties(gazetteer_year), gazetteer_year)
    await upsert_county_subdivisions(await download_county_subdivisions(gazetteer_year), gazetteer_year)
