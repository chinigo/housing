from asyncio import run

from housing.flow.root import root

if __name__ == "__main__":
    run(root.serve('Root Deployment', parameters={'year': 2023, 'state_postal_codes': ['NY']}))
