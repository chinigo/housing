import asyncio
import os
from logging.config import fileConfig

from housing.model import Base
from housing.model.gazetteer import *
from housing.model.tiger import *

from alembic import context
from geoalchemy2.alembic_helpers import include_object, render_item, writer
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

housing_db_url = os.environ.get('HOUSING_DB_CONNECTION_URL')

if housing_db_url is None:
    raise ValueError(
        'Must provide HOUSING_DB_CONNECTION_URL environment variable')

config.set_main_option('sqlalchemy.url', housing_db_url)


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        include_schemas=True,
        target_metadata=Base.metadata,
        include_object=include_object,
        process_revision_directives=writer,
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


asyncio.run(run_async_migrations())
