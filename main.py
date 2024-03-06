from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.gazetteer_ftp import GazetteerFTP
from housing.block.reference_ftp import ReferenceFTP
from housing.block.tiger_ftp import TigerFTP
from housing.flow.root import root


def create_blocks(data_dir: str, year: int):
    GazetteerFTP(gazetteer_year=year).save(name=f'gazetteer-ftp-{year}', overwrite=True)
    ReferenceFTP().save(name='reference-ftp', overwrite=True)
    TigerFTP(tiger_year=year).save(name=f'tiger-ftp-{year}', overwrite=True)
    CensusLocalFileSystem(basepath=f'{data_dir}/tiger-{year}').save(name=f'tiger-local-{year}', overwrite=True)
    CensusLocalFileSystem(basepath=f'{data_dir}/gazetteer-{year}').save(name=f'gazetteer-local-{year}', overwrite=True)
    CensusLocalFileSystem(basepath=f'{data_dir}/reference').save(name='reference-local', overwrite=True)


if __name__ == "__main__":
    create_blocks('/Users/mchinigo/workspace/repos/github.com/chinigo/housing/data', 2023)
    root.serve('Root Deployment', parameters={'year': 2023})
