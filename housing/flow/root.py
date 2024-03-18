from prefect import flow

from housing import AreaSpecifier
from housing.flow.download_gazetteer import download_gazetteer
from housing.flow.download_tiger import download_tiger

default_area_specifier: AreaSpecifier = {
        'NY': 'all',
        'VT': ['Rutland County', 'Bennington County', 'Addison County'],
    }

@flow(name='Root', persist_result=True)
def root(year: int, area_specifier: AreaSpecifier) -> None:
    download_gazetteer(year)
    download_tiger(year, area_specifier)
