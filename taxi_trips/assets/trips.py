import duckdb
import os
from dagster_duckdb import DuckDBResource
import requests
from . import constants
from dagster import asset, AssetExecutionContext
from ..partitions import monthly_partition

@asset(
    compute_kind='NYC Open Data API',
)
def tax_zones_file() -> None:
    '''The raw csv file for taxi zones dataset. Sourced from NYC Open Data portal.'''
    raw_taxi_zones = requests.get(
            'https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD'
        )
    with open(constants.TAXI_ZONES_FILE_PATH, 'wb') as f:
        f.write(raw_taxi_zones.content)

@asset(
    deps=['tax_zones_file'],
    compute_kind='DuckDB',
)
def taxi_zones(database: DuckDBResource) -> None:
    '''The raw taxi zones dataset, loaded into a DuckDB table.'''
    sql_query = f'''
    create or replace table zones as (
        select 
            LocationID as zone_id,
            borough as borough,
            zone as zone,
            the_geom as geometry
        from '{constants.TAXI_ZONES_FILE_PATH}'
    );
    '''
    with database.get_connection() as conn:
        conn.execute(sql_query)

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
    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), 'wb') as f:
        f.write(raw_trips.content)

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
      create table if not exists trips (
        vendor_id integer, pickup_zone_id integer, dropoff_zone_id integer,
        rate_code_id double, payment_type integer, dropoff_datetime timestamp,
        pickup_datetime timestamp, trip_distance double, passenger_count double,
        total_amount double, partition_date varchar
      );

      delete from trips where partition_date = '{month_to_fetch}';

      insert into trips
      select
        VendorID, PULocationID, DOLocationID, RatecodeID, payment_type, tpep_dropoff_datetime,
        tpep_pickup_datetime, trip_distance, passenger_count, total_amount, '{month_to_fetch}' as partition_date
      from '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)}';
    """

    with database.get_connection() as conn:
        conn.execute(query)

