from asyncio import run

from housing.flow.download_gazetteer import download_gazetteer
from housing.flow.download_tiger import download_tiger
from housing.flow.root import default_area_specifier, root


async def tiger() -> None:
    await download_tiger(2023, default_area_specifier)


async def gazetteer() -> None:
    await download_gazetteer(2023)

if __name__ == "__main__":
    # root(2023, default_area_specifier)
    run(tiger())
