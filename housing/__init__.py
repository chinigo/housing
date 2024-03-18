from pathlib import Path
from typing import Literal

from geopandas import options
options.io_engine = 'pyogrio'

data_dir = Path(__file__).resolve().joinpath('..', '..', 'data').resolve()

StatePostalCode = str
CountyName = str

AreaSpecifier = dict[StatePostalCode, list[CountyName] | Literal['all']]
