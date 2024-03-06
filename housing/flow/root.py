from prefect import flow

from housing.flow.download_gazetteer import download_gazetteer
from housing.flow.download_tiger import download_tiger


@flow(name='Root', persist_result=True)
def root(year: int):
    download_gazetteer(year)
    download_tiger(year)
