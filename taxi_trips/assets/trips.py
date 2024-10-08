import duckdb
import os
from dagster_duckdb import DuckDBResource
import requests
from dagster import asset, AssetExecutionContext
from taxi_trips.partitions import monthly_partition
from taxi_trips.assets.constants import FILE_PATH_TAXI_ZONES, FILE_PATH_TAXI_TRIPS_TEMPLATE

# Asset definitions

# Extract asset to generate file with taxi zones data
@asset(
    compute_kind='NYC Open Data API',
)
def tax_zones_file() -> None:
    '''The raw csv file for taxi zones dataset. Sourced from NYC Open Data portal.'''
    raw_taxi_zones = requests.get(
            'https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD'
        )
    with open(FILE_PATH_TAXI_ZONES, 'wb') as f:
        f.write(raw_taxi_zones.content)

# Extract asset to generate file with taxi trips data
@asset(
    partitions_def=monthly_partition,
    compute_kind='NYC Open Data API',
)
def taxi_trips_file(context: AssetExecutionContext) -> None:
    '''The raw parquet files for taxi trips dataset. Sourced from NYC Open Data portal.'''
    partition_date_str = context.partition_key
    month_to_fetch = partition_date_str[:-3]
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )
    with open(FILE_PATH_TAXI_TRIPS_TEMPLATE.format(month_to_fetch), 'wb') as f:
        f.write(raw_trips.content)

# Load asset to load taxi zones in DuckDB
@asset(
    deps=['tax_zones_file'],
    compute_kind='DuckDB',
)
def taxi_zones(database: DuckDBResource) -> None:
    '''The raw taxi zones dataset, loaded into a DuckDB table.'''
    sql_query = f'''
    CREATE OR REPLACE TABLE zones AS (
        SELECT
            LocationID as zone_id,
            borough,
            zone,
            the_geom as geometry
        FROM '{FILE_PATH_TAXI_ZONES}'
    );
    '''
    with database.get_connection() as conn:
        conn.execute(sql_query)

# Load asset to load taxi trips in DuckDB
@asset(
    deps=['taxi_trips_file'],
    partitions_def=monthly_partition,
    compute_kind='DuckDB',
)
def taxi_trips(context: AssetExecutionContext, database: DuckDBResource) -> None:
    '''The raw taxi trips dataset, loaded into a DuckDB table.'''
    # For every file in TAXI_TRIPS_TEMPLATE_FILE_PATH, extract the month to fetch and load it into the DuckDB table
    partition_date_str = context.partition_key
    month_to_fetch = partition_date_str[:-3]
    query = f"""
      CREATE TABLE IF NOT EXISTS trips (
        vendor_id integer,
        pickup_zone_id integer,
        dropoff_zone_id integer,
        rate_code_id double,
        payment_type integer,
        dropoff_datetime timestamp,
        pickup_datetime timestamp,
        trip_distance double,
        passenger_count double,
        total_amount double,
        partition_date varchar
    );
    DELETE FROM trips 
    WHERE partition_date = '{month_to_fetch}';
    INSERT INTO trips
    SELECT
    VendorID,
    PULocationID AS PICKUP_ZONE_ID,
    DOLocationID AS DROPOFF_ZONE_ID,
    RatecodeID,
    payment_type,
    tpep_dropoff_datetime, 
    tpep_pickup_datetime,
    trip_distance,
    passenger_count,
    total_amount,
    '{month_to_fetch}' AS PARTITION_DATE
    FROM '{FILE_PATH_TAXI_TRIPS_TEMPLATE.format(month_to_fetch)}';
    """
    with database.get_connection() as conn:
        conn.execute(query)

# Transformation asset to clean and transform the taxi trips data
@asset(
    deps=['taxi_trips'],  # Depend on the `taxi_trips` asset to ensure data is loaded before transformations
    partitions_def=monthly_partition,
    compute_kind='DuckDB'
)
def transformed_taxi_trips(context: AssetExecutionContext, database: DuckDBResource) -> None:
    '''Transformation step for the taxi trips dataset.
    Adds a day_of_week column and replaces NULL passenger counts with 0.'''
    partition_date_str = context.partition_key
    month_to_fetch = partition_date_str[:-3]
    
    transformation_query = f"""
    -- Create the transformed_trips table if it doesn't exist
    CREATE TABLE IF NOT EXISTS transformed_trips AS
    SELECT
        *,
        strftime('%w', pickup_datetime) AS day_of_week, -- Extract day of the week from pickup_datetime
        CASE 
            WHEN passenger_count IS NULL THEN 0 
            ELSE passenger_count 
        END AS passenger_count_transformed -- Replace NULL passenger counts with 0
    FROM trips
    WHERE 1=2; -- No data is inserted here; only table structure is created
    
    -- Delete any existing data for the current partition
    DELETE FROM transformed_trips WHERE partition_date = '{month_to_fetch}';
    
    -- Insert transformed data for the current partition
    INSERT INTO transformed_trips
    SELECT
        *,
        strftime('%w', pickup_datetime) AS day_of_week, -- Extract day of the week from pickup_datetime
        CASE 
            WHEN passenger_count IS NULL THEN 0 
            ELSE passenger_count 
        END AS passenger_count_transformed -- Replace NULL passenger counts with 0
    FROM trips
    WHERE partition_date = '{month_to_fetch}';
    """
    with database.get_connection() as conn:
        conn.execute(transformation_query)