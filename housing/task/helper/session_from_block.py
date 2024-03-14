from contextlib import asynccontextmanager
from typing import AsyncGenerator

from prefect_sqlalchemy import SqlAlchemyConnector
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def session_from_block(db_block: SqlAlchemyConnector) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(db_block.get_engine()) as sess:
        yield sess
