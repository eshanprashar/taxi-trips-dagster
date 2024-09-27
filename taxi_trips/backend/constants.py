import os

# Get the base directory where the script is running (assuming this is constants.py's location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the base directory where the script is running (assuming this is constants.py's location)
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "staging", "data.duckdb")