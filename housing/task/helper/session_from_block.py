from contextlib import asynccontextmanager
from typing import AsyncGenerator

from prefect_sqlalchemy import SqlAlchemyConnector
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.base import Engine


@asynccontextmanager
async def session_from_block(db_block: SqlAlchemyConnector) -> AsyncGenerator[AsyncSession, None]:
    engine = db_block.get_engine(execution_options={'preserve_rowcount': True})

    if isinstance(engine, Engine):
        raise ValueError('Expected AsyncEngine, got Engine')

    async with AsyncSession(engine) as session:
        yield session
