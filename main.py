from housing.flow.root import root


if __name__ == "__main__":
    root.serve('Root Deployment', parameters={'year': 2023, 'state_codes_of_interest': ['NY']})
