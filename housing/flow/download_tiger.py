from prefect import flow

from housing.task.tiger.download_coastlines import download_coastlines


@flow(name='Download TIGER source files', persist_result=True)
def download_tiger(tiger_year: int, _state_postal_codes: list[str]):
    download_coastlines(tiger_year)
