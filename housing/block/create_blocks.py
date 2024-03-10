# from os import environ
#
# from prefect_sqlalchemy import AsyncDriver, ConnectionComponents, SqlAlchemyConnector
#
# from housing import data_dir
# from housing.block.census_local_filesystem import CensusLocalFileSystem
# from housing.block.gazetteer_ftp import GazetteerFTP
# from housing.block.reference_ftp import ReferenceFTP
# from housing.block.tiger_ftp import TigerFTP
#
#
# def create_blocks(year: int):
#     GazetteerFTP(gazetteer_year=year).save(name=f'gazetteer-ftp-{year}', overwrite=True)
#     ReferenceFTP().save(name='reference-ftp', overwrite=True)
#     TigerFTP(tiger_year=year).save(name=f'tiger-ftp-{year}', overwrite=True)
#     CensusLocalFileSystem(basepath=f'{data_dir}/tiger-{year}').save(name=f'tiger-local-{year}', overwrite=True)
#     CensusLocalFileSystem(basepath=f'{data_dir}/gazetteer-{year}').save(name=f'gazetteer-local-{year}', overwrite=True)
#     CensusLocalFileSystem(basepath=f'{data_dir}/reference').save(name='reference-local', overwrite=True)
#     CensusLocalFileSystem(basepath=f'{data_dir}/included').save(name='included-local', overwrite=True)
#     SqlAlchemyConnector(
#         connection_info=ConnectionComponents(
#             driver=AsyncDriver.POSTGRESQL_ASYNCPG,
#             username=environ.get('HOUSING_DB_USERNAME'),
#             password=environ.get('HOUSING_DB_PASSWORD'),
#             host=environ.get('HOUSING_DB_HOST'),
#             port=environ.get('HOUSING_DB_PORT'),
#             database=environ.get('HOUSING_DB_DATABASE'),
#         ),
#     ).save('housing-database', overwrite=True)
