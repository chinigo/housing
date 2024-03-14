from logging import Logger, LoggerAdapter
from os import environ
from typing import Any, Optional, TypeVar, cast

from prefect import get_run_logger
from prefect.blocks.core import Block
from prefect.runtime import flow_run, task_run
from prefect_sqlalchemy import AsyncDriver, ConnectionComponents, SqlAlchemyConnector

from housing import data_dir
from housing.block.census_local_filesystem import CensusLocalFileSystem
from housing.block.gazetteer_ftp import GazetteerFTP
from housing.block.reference_ftp import ReferenceFTP
from housing.block.tiger_ftp import TigerFTP

T = TypeVar('T', bound='Block')


class Registry:
    _instance: Optional["Registry"] = None
    _logger: Optional[Logger | LoggerAdapter[Any]] = None

    def __new__(cls) -> "Registry":
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
            cls._logger = get_run_logger()

        if cls._instance is None:
            raise ValueError('Could not instantiate block Registry')

        return cls._instance

    @classmethod
    async def _load_or_create_block(cls, block: T, block_name: str) -> T:
        if cls._logger is None:
            raise ValueError('Logger is undefined')

        try:
            cls._logger.debug(f'Loading {block.__class__.__name__} block {block_name}')
            return cast(T, await block.load(block_name))
        except ValueError as e:
            cls._logger.debug(str(e))
            cls._logger.info(f'Creating {block.__class__.__name__} block {block_name}')

            await block.save(name=block_name)

            return block

    @classmethod
    def _flow_params(cls, key: str) -> Any:
        return flow_run.parameters[key]

    @classmethod
    def _task_params(cls, key: str) -> Any:
        return task_run.parameters[key]

    @classmethod
    async def gazetteer_ftp(cls) -> GazetteerFTP:
        return await cls._load_or_create_block(
            GazetteerFTP(gazetteer_year=cls._flow_params('gazetteer_year')),
            f'gazetteer-ftp-{cls._flow_params('gazetteer_year')}')

    @classmethod
    async def housing_database(cls) -> SqlAlchemyConnector:
        return await cls._load_or_create_block(
            SqlAlchemyConnector(
                connection_info=ConnectionComponents(
                    driver=AsyncDriver.POSTGRESQL_ASYNCPG,
                    username=environ.get('HOUSING_DB_USERNAME'),
                    password=environ.get('HOUSING_DB_PASSWORD'),
                    host=environ.get('HOUSING_DB_HOST'),
                    port=environ.get('HOUSING_DB_PORT'),
                    database=environ.get('HOUSING_DB_DATABASE'),
                ),
            ),
            'housing-database',
        )

    @classmethod
    async def local_data(cls) -> CensusLocalFileSystem:
        return await cls._load_or_create_block(
            CensusLocalFileSystem(basepath=str(data_dir.joinpath('local'))),
            f'local-data',
        )

    @classmethod
    async def reference_ftp(cls) -> ReferenceFTP:
        return await cls._load_or_create_block(ReferenceFTP(), 'reference-ftp')

    @classmethod
    async def reference_local(cls) -> CensusLocalFileSystem:
        return await cls._load_or_create_block(
            CensusLocalFileSystem(basepath=str(data_dir.joinpath(f'reference-local'))),
            f'reference-local',
        )

    @classmethod
    async def tiger_ftp(cls) -> TigerFTP:
        return await cls._load_or_create_block(
            TigerFTP(tiger_year=cls._flow_params('tiger_year')),
            f'tiger-ftp-{cls._flow_params('tiger_year')}'
        )

    @classmethod
    async def tiger_local(cls) -> CensusLocalFileSystem:
        return await cls._load_or_create_block(
            CensusLocalFileSystem(basepath=str(data_dir.joinpath(f'tiger-local-{cls._flow_params('tiger_year')}'))),
            f'tiger-local-{cls._flow_params('tiger_year')}',
        )

    @classmethod
    async def gazetteer_local(cls) -> CensusLocalFileSystem:
        return await cls._load_or_create_block(
            CensusLocalFileSystem(
                basepath=str(data_dir.joinpath(f'gazetteer-local-{cls._flow_params('gazetteer_year')}'))
            ),
            f'gazetteer-local-{cls._flow_params('gazetteer_year')}',
        )
