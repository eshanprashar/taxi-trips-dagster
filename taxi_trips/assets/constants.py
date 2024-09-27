import os

# Get the base directory where the script is running (assuming this is constants.py's location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set paths relative to the base directory
TAXI_ZONES_FILE_PATH = os.path.join(BASE_DIR, "data", "raw", "taxi_zones.csv")
TAXI_TRIPS_TEMPLATE_FILE_PATH = os.path.join(BASE_DIR, "data", "raw", "taxi_trips_{}.parquet")

TRIPS_BY_AIRPORT_FILE_PATH = os.path.join(BASE_DIR, "data", "outputs", "trips_by_airport.csv")
TRIPS_BY_WEEK_FILE_PATH = os.path.join(BASE_DIR, "data", "outputs", "trips_by_week.csv")
MANHATTAN_STATS_FILE_PATH = os.path.join(BASE_DIR, "data", "staging", "manhattan_stats.geojson")
MANHATTAN_MAP_FILE_PATH = os.path.join(BASE_DIR, "data", "outputs", "manhattan_map.png")

REQUEST_DESTINATION_TEMPLATE_FILE_PATH = os.path.join(BASE_DIR, "data", "outputs", "{}.png")


DATE_FORMAT = "%Y-%m-%d"

START_DATE = "2023-01-01"
END_DATE = "2024-01-01" # Changed this to get data for 12 months