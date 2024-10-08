from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import duckdb
from taxi_trips.backend import constants

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Taxi Trips API! Use /trips_monthly to fetch data."}

@app.get("/trips_monthly")
def get_monthly_trips():
    query = """
    SELECT partition_date, COUNT(*) as trip_count
    FROM trips
    GROUP BY partition_date
    ORDER BY partition_date
    """
    conn = duckdb.connect(constants.DUCKDB_PATH)
    df = conn.execute(query).fetch_df()
    return df.to_dict(orient='records')

@app.get("/trips_monthly_by_borough")
def get_monthly_trips_by_borough():
    query = """
        SELECT 
            zones.borough, 
            trips.partition_date,
            COUNT(*) as num_trips
        FROM trips
        LEFT JOIN zones ON trips.pickup_zone_id = zones.zone_id
        WHERE zones.borough IS NOT NULL
        GROUP BY zones.borough, trips.partition_date
        ORDER BY trips.partition_date, zones.borough;
    """
    conn = duckdb.connect(constants.DUCKDB_PATH)
    df = conn.execute(query).fetch_df()
    return df.to_dict(orient='records')
    
