from prefect import flow

from housing import AreaSpecifier
from housing.flow.download_reference import download_reference
from housing.flow.download_tiger import download_tiger

default_area_specifier: AreaSpecifier = {
        'NY': 'all',
    }

@flow(name='All', persist_result=True)
def all(year: int, area_specifier: AreaSpecifier) -> None:
    download_reference()
    download_tiger(year, area_specifier)
