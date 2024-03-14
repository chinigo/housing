from prefect import flow

from housing.task.tiger.download_coastlines import download_coastlines


@flow(name='Download TIGER source files', persist_result=True)
async def download_tiger(tiger_year: int, state_postal_codes: list[str]) -> None:
    await download_coastlines(tiger_year)
