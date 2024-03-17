from housing.flow.download_tiger import download_tiger
from housing.flow.download_gazetteer import download_gazetteer
from housing.flow.root import root
from asyncio import run


async def tiger() -> None:
    await download_tiger(2023, ['NY', 'VT'])


async def gazetteer() -> None:
    await download_gazetteer(2023)

if __name__ == "__main__":
    root(2023, ['NY', 'VT'])
