from asyncio import run

from housing.flow.all import default_area_specifier, all

if __name__ == "__main__":
    run(all.serve('Root Deployment', parameters={'year': 2023, 'area_specifier': default_area_specifier}))
