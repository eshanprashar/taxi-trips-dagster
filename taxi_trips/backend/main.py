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
    return {"message": "Welcome to the Taxi Trips API! Use /monthly_trips to fetch data."}

@app.get("/monthly_trips")
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
