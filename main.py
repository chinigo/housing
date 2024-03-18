from asyncio import run

from housing.flow.root import default_area_specifier, root

if __name__ == "__main__":
    run(root.serve('Root Deployment', parameters={'year': 2023, 'area_specifier': default_area_specifier}))
