import os

# Get the base directory where the script is running (assuming this is constants.py's location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# FILE PATHS
FILE_PATH_TAXI_ZONES = os.path.join(BASE_DIR, "data", "raw", "taxi_zones.csv")
FILE_PATH_TAXI_TRIPS_TEMPLATE = os.path.join(BASE_DIR, "data", "raw", "taxi_trips_{}.parquet")
FILE_PATH_TRIPS_BY_AIRPORT = os.path.join(BASE_DIR, "data", "outputs", "trips_by_airport.csv")
FILE_PATH_TRIPS_BY_WEEK = os.path.join(BASE_DIR, "data", "outputs", "trips_by_week.csv")
FILE_PATH_MANHATTAN_STATS = os.path.join(BASE_DIR, "data", "staging", "manhattan_stats.geojson")
FILE_PATH_MANHATTAN_MAP = os.path.join(BASE_DIR, "data", "outputs", "manhattan_map.png")
FILE_PATH_REQUEST_DESTINATION_TEMPLATE = os.path.join(BASE_DIR, "data", "outputs", "{}.png")

# Date Constants
DATE_FORMAT = "%Y-%m-%d"
START_DATE = "2023-01-01"
END_DATE = "2024-01-01"