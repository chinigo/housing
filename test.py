from asyncio import run

from housing.flow import default_area_specifier, download_reference, download_tiger, all


async def tiger() -> None:
    await download_tiger(2023, default_area_specifier)


async def reference() -> None:
    await download_reference()

if __name__ == "__main__":
    # root(2023, default_area_specifier)
    # run(tiger())
    run(reference())
