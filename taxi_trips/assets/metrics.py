from dagster import asset
import plotly.express as px
import plotly.io as pio
import geopandas as gpd

import os
import duckdb
from datetime import datetime, timedelta
from dagster_duckdb import DuckDBResource
import pandas as pd

from taxi_trips.assets.constants import FILE_PATH_MANHATTAN_STATS, FILE_PATH_MANHATTAN_MAP, DATE_FORMAT, FILE_PATH_TRIPS_BY_WEEK

@asset(
    deps=['transformed_taxi_trips','taxi_zones']
)
def manhattan_stats(database:DuckDBResource) -> None:
    query = '''
        SELECT
            z.zone,
            z.borough,
            z.geometry,
            count(1) as num_trips,
        FROM transformed_trips as t
        LEFT JOIN zones AS z on t.pickup_zone_id = z.zone_id
        WHERE borough = 'Manhattan' AND geometry IS NOT NULL AND t.passenger_count_transformed > 0
        GROUP BY zone, borough, geometry
    '''
    with database.get_connection() as conn:
        trips_by_zone = conn.execute(query).fetch_df()

    trips_by_zone['geometry'] = gpd.GeoSeries.from_wkt(trips_by_zone['geometry'])
    trips_by_zone = gpd.GeoDataFrame(trips_by_zone)

    with open(FILE_PATH_MANHATTAN_STATS, 'w') as f:
        f.write(trips_by_zone.to_json())

@asset(
    deps=['manhattan_stats'],
)
def manhattan_map() -> None:
    trips_by_zone = gpd.read_file(FILE_PATH_MANHATTAN_STATS)

    fig = px.choropleth_mapbox(trips_by_zone,
        geojson=trips_by_zone.geometry.__geo_interface__,
        locations=trips_by_zone.index,
        color='num_trips',
        color_continuous_scale="Plasma",
        mapbox_style="carto-positron",
        center={"lat": 40.7831, "lon": -73.9712},
        zoom=10,
        opacity=0.5,
        labels={'num_trips':'Number of Trips'}
    )
    pio.write_image(fig, FILE_PATH_MANHATTAN_MAP)

@asset(
    deps=['transformed_taxi_trips']
)
def trips_by_week(database:DuckDBResource)-> None:
    

    current_date = datetime.strptime("2023-03-01", DATE_FORMAT)
    end_date = datetime.strptime("2023-04-01", DATE_FORMAT)
    
    result = pd.DataFrame()
    
    # Fetch data for each week
    while current_date < end_date:
        current_date_str = current_date.strftime(DATE_FORMAT)
        # Fetch all relevant data in one go
        query = f'''
            SELECT
                vendor_id,
                total_amount, 
                trip_distance, 
                passenger_count_transformed
            FROM transformed_trips
            WHERE date_trunc('week',pickup_datetime) = date_trunc('week', '{current_date_str}'::date)
            AND passenger_count_transformed > 0
        '''
        with database.get_connection() as conn:
            week_data = conn.execute(query).fetch_df()
        
        aggregate = week_data.agg({
            'vendor_id': 'count',
            'total_amount': 'sum',
            'trip_distance': 'sum',
            'passenger_count_transformed': 'sum'
        }).rename({'vendor_id': 'num_trips'}).to_frame().T

        aggregate['period'] = current_date
        result = pd.concat([result, aggregate])

        current_date += timedelta(days=7)
    
    # clean up the formatting of the dataframe
    result['num_trips'] = result['num_trips'].astype(int)
    result['passenger_count_transformed'] = result['passenger_count_transformed'].astype(int)
    result['total_amount'] = result['total_amount'].round(2).astype(float)
    result['trip_distance'] = result['trip_distance'].round(2).astype(float)
    result = result[["period", "num_trips", "total_amount", "trip_distance", "passenger_count_transformed"]]
    result = result.sort_values(by="period")

    result.to_csv(FILE_PATH_TRIPS_BY_WEEK, index=False)