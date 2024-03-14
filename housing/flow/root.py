from prefect import flow

from housing.flow.download_gazetteer import download_gazetteer
from housing.flow.download_tiger import download_tiger


@flow(name='Root', persist_result=True)
def root(year: int, state_postal_codes: list[str]) -> None:
    download_gazetteer(year)
    download_tiger(year, state_postal_codes)
